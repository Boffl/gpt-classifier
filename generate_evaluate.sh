#!/bin/bash

task=$1
shots=$2  # zero_shot or 12_shot or what not
n=$3  # number of tweets for the progress bar

# call the generate script
if [ "$shots" = "zero_shot" ]; then

  python3.11 gpt-classifier.py raw_data/$task/test_text.txt raw_data/$task/classes.txt gpt_responses_$shots/$task.txt \
   --count_tokens api_usage_log/$task\_$shots.csv --number_of_tweets $n
else
    python3.11 gpt-classifier.py raw_data/$task/test_text.txt raw_data/$task/classes.txt gpt_responses_$shots/$task.txt \
   --few_shot raw_data/$task/examples.jsonl --count_tokens api_usage_log/$task\_$shots.csv --number_of_tweets $n
fi

python3.11 encode_predicions.py gpt_responses_$shots/$task.txt raw_data/$task/mappings.txt predictions_$shots/$task.txt


