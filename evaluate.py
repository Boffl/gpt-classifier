def preprocess_predictions(file):
    classes = ['anger', 'joy', 'optimism', 'sadness']
    predictions = []
    with open(file) as infile:
        for line in infile:
            for cl in classes:
                if line.startswith(cl):
                    predictions.append(cl)
    mapping = {'anger': 0, 'joy': 1, 'optimism': 2, 'sadness': 3}
    predictions = [ mapping[ pred ] for pred in predictions ]
    for pred in predictions:
        print(pred)
        with open('outfile.txt', 'a', encoding='utf-8') as writer:
            writer.write(f'{pred}\n')







preds = preprocess_predictions('predictions/emotion/test_1.txt')



