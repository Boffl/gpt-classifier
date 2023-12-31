# gpt-classifier
Using GPT as a classifier and testing it on the [tweeteval](https://github.com/cardiffnlp/tweeteval) benchmark dataset.
## classifying tweets with gpt:
The script ```gpt-classifier.py``` calls the openAI api to classify tweets given some classes,
it writes the responses into a file. 
example call:
```
python gpt-classifier.py raw_data\hate\test_text.txt raw_data\hate\classes.txt gpt_responses_zero_shot\hate.txt --count_tokens hate_zero_shot.csv --number_of_tweets 2970 --skip_lines 73
```

## turning the responses into encoded labels
To turn the responses from GPT into encoded labels (for the evaluation) use the ```encode_predictions.py```
script. Example call:
```
python encode_predictions.py gpt_responses_zero_shot/hate.txt raw_data/hate/mappings.txt predictions_zero_shot/hate.txt
```

## Evaluating on the tweeteval dataset
The file ```evaluate_script.py``` is taken from the Tweeteval repository, it returns the performance
compared to the gold standard. Example call:
```
python evaluate_script.py --tweeteval_path raw_data --predictions_path predictions_zero_shot --task hate
```

## Creating examples for the few shot setting
To choose random examples from the validation set to give to the model as few-shot input call 
```create_few_shot_examples.py```. In the call specify the task and number of examples (must be a multiple of the number of classes). You can define a data 
directory, the default is 'raw_data'. It will create a file ```examples.jsonl``` with random samples from the validation set. Example call:
```
python create_few_shot_examples.py hate 12 --data_dir raw_data
```