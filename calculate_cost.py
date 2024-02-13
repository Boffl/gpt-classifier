import sys
import os

infolder = sys.argv[1]
# price per 1k tokens
price_prompt = float(sys.argv[2])
price_gen = float(sys.argv[3])

# # Prices last year for gpt-3.5-turbo
# price_prompt = 0.001
# price_gen = 0.002


def count_cost_per_file(filepath):
    global cost
    with open(filepath, 'r', encoding='utf-8') as infile:
        for line in infile:
            prompt_toks, gen_toks = line.split(',')[0], line.split(',')[1].strip()

            cost += 0.001 * int(prompt_toks) * price_prompt + 0.001 * int(gen_toks) * price_gen


cost = 0
if os.path.isdir(infolder):
    for subdir, dirs, filenames in os.walk(infolder):
        for filename in filenames:
            filepath = os.path.join(subdir, filename)
            count_cost_per_file(filepath)

elif os.path.isfile(infolder):
    count_cost_per_file(infolder)

else:
    print(f"{infolder} is neither a filepath or directory")
    exit(1)

print(cost)
