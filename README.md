# gpt-classifier
Using GPT as a classifier and testing it on the [tweeteval](https://github.com/cardiffnlp/tweeteval) benchmark dataset.

## Results
We compare the results from GPT to the SOTA performance on the test sets indicated by the 
[Tweeteval Leaderboard](https://github.com/cardiffnlp/tweeteval/blob/main/README.md) <br>
The reported score corresponds to the F1-macro except for sentiment, where recall is used (this is in accordance
with the metrics used on the original task, check the [reference paper](https://arxiv.org/pdf/2010.12421.pdf) for details)

| Model | Emotion | Hate | Offensive | Sentiment | 
|----------|:------:|:--------:|:-----:|:------:| 
| GPT-3.5 (zero shot)   | 74.7     | 42.6       | 72.6    | 70.8   |
| GPT-3.5 (12 shot)   | 75.7     |  **69.9**     | 67.4    |  70.8    |
| GPT-4 (zero shot)   |   67.2   |  64.9      | 77.0    |     | 
| GPT-4 (12 shot)   |   **80.5**   |  62.8    | 69.9   |   |
| SOTA | 80.2  | 56.4   | **82.2**   |  73.7   |


## Usage of the scripts
### classify and evaluate
The bash script ```generate_evaluate.sh``` evokes the generation script that calls OpenAI's API, transforms the responses into labels and evaluates against the true labels.
It expects a folder structure similar to this repo, with all necessary directories to save results. <br>
As arguments the script takes
- The task ('Emotion', 'Hate', 'Offensive', 'Sentiment')
- The setting ('zero_shot' or 'few_shot)
    - if 'few_shot' there needs to be a file ```examples.jsonl``` with examples for the few shot case
- The number of tweets to be classified (needed for the progress bar)
- The model name
Example call:
```
bash generate_evaluate.sh hate zero_shot 2970 gpt-4
```
### classifying tweets with gpt:
The script ```gpt-classifier.py``` calls the openAI api to classify tweets given some classes,
it writes the responses into a file. 
example call:
```
python gpt-classifier.py raw_data\hate\test_text.txt raw_data\hate\classes.txt gpt_responses_zero_shot\hate.txt --count_tokens hate_zero_shot.csv --number_of_tweets 2970 --skip_lines 73
```

### turning the responses into encoded labels
To turn the responses from GPT into encoded labels use the ```encode_predictions.py```
script. Example call:
```
python encode_predictions.py gpt_responses_zero_shot/hate.txt raw_data/hate/mappings.txt predictions_zero_shot/hate.txt
```

### Evaluating on the tweeteval dataset
The file ```evaluate_script.py``` is taken from the Tweeteval repository, it returns the performance
compared to the gold standard. Example call:
```
python evaluate_script.py --tweeteval_path raw_data --predictions_path predictions_zero_shot --task hate
```

### Creating examples for the few shot setting
To choose random examples from the validation set to give to the model as few-shot input call 
```create_few_shot_examples.py```. In the call specify the task and number of examples (must be a multiple of the number of classes). You can define a data 
directory, the default is 'raw_data'. It will create a file ```examples.jsonl``` with random samples from the validation set. Example call:
```
python create_few_shot_examples.py hate 12 --data_dir raw_data
```