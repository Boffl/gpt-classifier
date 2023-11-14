import sys
import os

infolder = sys.argv[1]
price_prompt = 0.001
price_gen = 0.002

cost = 0
for filename in os.listdir(infolder):
    if filename == 'sentiment_12_shot.csv':
        continue

    filepath = os.path.join(infolder, filename)

    with open(filepath, 'r', encoding='utf-8') as infile:
        for line in infile:
            prompt_toks, gen_toks = line.split(',')[0], line.split(',')[1].strip()

            cost += 0.001*int(prompt_toks)*price_prompt + 0.001*int(gen_toks)*price_gen
print(cost)
