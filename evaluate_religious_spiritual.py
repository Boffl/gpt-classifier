from collections import Counter


def eval_data(task, prediction_file):
    with open(prediction_file) as pred_file:
        mapping = get_mapping(task)
        predictions = [ ]
        for line in pred_file:
            line = line.rstrip('\n')
            pred = mapping[ line ]
            predictions.append(pred)

        class_count = Counter(predictions, )
        return class_count


def get_mapping(task):
    with open(f'raw_data/{task}/mapping.txt', "r", encoding='utf-8') as map_file:
        mapping = {}
        for line in map_file:
            line = line.rstrip('\n')
            line = line.split()
            mapping[ line[ 0 ] ] = line[ 1 ]
        return mapping


def compare_spirit_religion(task):
    spiritual_file = f'predictions_zero_shot/spirituality_{task}.txt'
    religious_file = f'predictions_zero_shot/religion_{task}.txt'

    spiritual_result = eval_data(task, spiritual_file).most_common()
    religious_result = eval_data(task, religious_file).most_common()

    print(f' Spiritual results: {spiritual_result}')
    print(f' Religious_result: {religious_result}')









def main():
    task = 'sentiment'

    compare_spirit_religion(task)
if __name__ == '__main__':
    main()
