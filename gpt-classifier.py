import json
import os
import tiktoken
from openai import OpenAI

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
    print(classify('I love you', ['positive', 'negative']))