#!/bin/bash

task=$1
shots=$2  # zero_shot or 12_shot or what not
n=$3  # number of tweets for the progress bar
if [ -z "$4" ]; then
    model="gpt-3"
else
    model="$4"
fi

# call the generate script
if [ "$shots" = "zero_shot" ]; then

  python3.11 gpt-classifier.py "raw_data/${task}/test_text.txt" "raw_data/${task}/classes.txt" "${model}_responses/${shots}/${task}.txt" \
   --count_tokens "api_usage_log/${model}/${task}_${shots}.csv" --number_of_tweets $n --model_name "${model}"
else
    python3.11 gpt-classifier.py "raw_data/${task}/test_text.txt" "raw_data/${task}/classes.txt" "${model}_responses/${shots}/${task}.txt" \
   --few_shot "raw_data/${task}/examples.jsonl" --count_tokens "api_usage_log/${model}/${task}_${shots}.csv" --number_of_tweets $n --model_name "${model}"
fi

python3.11 encode_predictions.py "${model}_responses/${shots}/${task}.txt" "raw_data/${task}/mapping.txt" "${model}_predictions/${shots}/${task}.txt"

python3.11 evaluate_script.py --tweeteval_path "raw_data/" --predictions_path "${model}_predictions/${shots}/" --task "${task}"
