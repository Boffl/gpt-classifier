from argparse import ArgumentParser

def get_enc_labels(filepath, mapping):
    '''turn the gpt generated classes into encoded labels'''
    print(mapping)
    predictions = []
    with open(filepath) as infile:
        for line in infile:
            for label in mapping:
                if line.startswith(label):
                    predictions.append(label)

    return [mapping[pred] for pred in predictions]


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('mappingfile')
    parser.add_argument('outfile')
    args = parser.parse_args()

    mapping = {}
    with open(args.mappingfile, 'r', encoding='utf-8') as reader:
        for line in reader:
            label_enc, label_text = line.split()[0], line.split()[1].strip()
            mapping[label_text] = label_enc

    preds = get_enc_labels(args.infile, mapping)
    with open(args.outfile, 'w', encoding='utf-8') as outfile:
        for pred in preds:
            outfile.write(f'{pred}\n')



