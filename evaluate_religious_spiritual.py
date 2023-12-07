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
    total_spirit = 930
    total_religious = 1067

    spiritual_file = f'predictions_zero_shot/spirituality_{task}.txt'
    religious_file = f'predictions_zero_shot/religion_{task}.txt'

    spiritual_result = eval_data(task, spiritual_file)
    religious_result = eval_data(task, religious_file)

    class_percentages_spirit = {key: (count / total_spirit) for key, count in spiritual_result.items()}
    class_percentages_religious = {key: (count / total_religious) for key, count in religious_result.items()}

    mapping = get_mapping(task)

    for maps in mapping.values():
        print(f' {maps} : Religious = {class_percentages_religious[maps]:.3f} , Spiritual = {class_percentages_spirit[maps]:.3f}')




   # print(f' Spiritual results: {spiritual_result}')
   # print(f' Religious_result: {religious_result}')




def main():


    print('HATE SUBTASK')
    compare_spirit_religion('hate')

    print('-'*77)

    print('OFFENSIVE SUBTASK')
    compare_spirit_religion('offensive')
    print('-' * 77)

    print('EMOTION SUBTASK')
    compare_spirit_religion('emotion')
    print('-' * 77)

    print('SENTIMENT SUBTASK')
    compare_spirit_religion('sentiment')







if __name__ == '__main__':
    main()
