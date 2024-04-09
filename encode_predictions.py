from argparse import ArgumentParser

def get_enc_labels(filepath, mapping):
    '''turn the gpt generated classes into encoded labels
    inputs: 1) filepath to the file with GPTs generations
            2) a dictionary with {"label_name":0, etc}

    returns: a list of label encodings
    '''
    print(mapping)
    predictions = []
    with open(filepath) as infile:
        for line in infile:
            for label in mapping:
                if line.startswith(label):
                    predictions.append(label)

    return [mapping[pred] for pred in predictions]

def get_mapping(mappingfile):
    mapping = {}
    with open(mappingfile, 'r', encoding='utf-8') as reader:
        for line in reader:
            label_enc, label_text = line.split()[0], line.split()[1].strip()
            mapping[label_text] = label_enc
    return mapping

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('infile', help="a file with the response to a tweet from GPT on each line, as created by the gpt-classifier")
    parser.add_argument('mappingfile', help="a tsv file with the encoding and the corresponding label")
    parser.add_argument('outfile', help="filepath where the encoded labels (predictions) should be saved")
    args = parser.parse_args()

    mapping = get_mapping(args.mappingfile)

    preds = get_enc_labels(args.infile, mapping)
    with open(args.outfile, 'w', encoding='utf-8') as outfile:
        for pred in preds:
            outfile.write(f'{pred}\n')



