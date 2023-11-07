import json
import os
import tiktoken
from openai import OpenAI
import jsonlines
from tqdm import tqdm
from argparse import ArgumentParser

api_key = os.getenv('OPENAI_KEY')
org_id = os.getenv('ORG_ID')

# set api-key for authentication, privat or organizational
if org_id:
    print('this')
    client = OpenAI(api_key=api_key, organization= org_id)
else:
    client = OpenAI(api_key=api_key)


def make_logit_bias(inputs:list[str], model='gpt-3.5-turbo'):
    """
    returns:  1) a dictionary setting all the ids of the corresponding BPE tokens to 100
              2) The highest number of BPE tokens among the inputs (to set max_len when generating)
    """
    logit_bias = {}
    encoder = tiktoken.encoding_for_model(model)
    max_toks = 0  # the maximum number of tokens needed for writing the inputs
    for input in inputs:
        encoding = encoder.encode(input)
        max_toks = max(len(encoding), max_toks)
        for tokenid in encoding:
            logit_bias[tokenid] = 100

    return logit_bias, max_toks



def classify(text:str, classes:list[str], examples=[], model='gpt-3.5-turbo'):

    logit_bias, max_tokens = make_logit_bias(classes)

    # setting up the messages
    # system message
    messages = [
    {"role": "system",
     "content": f"You are a helpful assistant, tasked with classifying the user input according to following classes: {', '.join(classes)}"}]

    # append the examples (few-shot)
    for message in examples:
        messages.append(message)

    # add the tweet that is to be classified
    messages.append({"role": "user", "content": text})

    completion = client.chat.completions.create(
      model=model,
      messages=messages,
        logit_bias=logit_bias,
        max_tokens=max_tokens,
        top_p=0.1

    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('filepath_tweets')
    parser.add_argument('filepath_classes')
    parser.add_argument('outfilepath')
    parser.add_argument('--few_shot', default='')
    parser.add_argument('--number_of_tweets', help="total number of tweets to classify, for the progress bar")
    args = parser.parse_args()

    total_number = int(args.number_of_tweets)

    examples = []
    if args.few_shot:
        with jsonlines.open(args.few_shot) as reader:
            for line in reader:
                examples.append(line)

    classes = []
    with open(args.filepath_classes, 'r', encoding='utf-8') as reader:
        for line in reader:
            classes.append(line.strip())


    with open(args.filepath_tweets, 'r', encoding='utf-8') as reader:
        with open(args.outfilepath, 'w', encoding='utf-8') as writer:
            for line in tqdm(reader, total=total_number):
                prediction = classify(line, classes, examples=examples)
                writer.write(f'{prediction}\n')