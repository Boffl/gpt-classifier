#!/bin/bash

task=$1
shots=$2  # zero_shot or 12_shot or what not
n=$3  # number of tweets for the progress bar
model=$4
if [ -z "$5" ]; then
    prompt="You are a helpful assistant, tasked with classifying the user input according to following classes: "
    prompt_dir=""
else
    prompt="$5"
    prompt_dir="specific_prompt/"
fi

responses_dir="${model}_responses/${shots}/${prompt_dir}"
predictions_dir="${model}_predictions/${shots}/${prompt_dir}"

# call the generate script
if [ "$shots" = "zero_shot" ]; then

  python3.11 gpt-classifier.py "raw_data/${task}/test_text.txt" "raw_data/${task}/classes.txt" "${responses_dir}${task}.txt" \
   --count_tokens "api_usage_log/${model}/${prompt_dir}${task}_${shots}.csv" --number_of_tweets $n --model_name "${model}" \
   --prompt "${prompt}"
else
    python3.11 gpt-classifier.py "raw_data/${task}/test_text.txt" "raw_data/${task}/classes.txt" "${responses_dir}${task}.txt" \
   --few_shot "raw_data/${task}/examples.jsonl" --count_tokens "api_usage_log/${model}/${prompt_dir}${task}_${shots}.csv" --number_of_tweets $n \
    --model_name "${model}" --prompt "${prompt}"
fi

python3.11 encode_predictions.py "${responses_dir}${task}.txt" "raw_data/${task}/mapping.txt" "${predictions_dir}${task}.txt"

python3.11 evaluate_script.py --tweeteval_path "raw_data/" --predictions_path "${predictions_dir}" --task "${task}"
