from collections import Counter
import numpy as np


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
    total_spirit = 942
    total_religious = 1059

    spiritual_file = f'predictions_zero_shot/spirituality_{task}_3.txt'
    religious_file = f'predictions_zero_shot/religion_{task}_3.txt'

    spiritual_result = eval_data(task, spiritual_file)
    religious_result = eval_data(task, religious_file)

    class_percentages_spirit = {key: (count / total_spirit) for key, count in spiritual_result.items()}
    class_percentages_religious = {key: (count / total_religious) for key, count in religious_result.items()}

    mapping = get_mapping(task)

    for maps in mapping.values():
        print(
            f' {maps} : Religious = {class_percentages_religious[ maps ]:.3f} , Spiritual = {class_percentages_spirit[ maps ]:.3f}')


# print(f' Spiritual results: {spiritual_result}')
# print(f' Religious_result: {religious_result}')


def calculate_mean_std(filepath, task):
    file_1 = f"{filepath}_{task}.txt"
    file_2 = f"{filepath}_{task}_2.txt"
    file_3 = f"{filepath}_{task}_3.txt"

    with open(file_1) as file:
        total_size_1 = 0
        for line in file:
            total_size_1 += 1

    with open(file_2) as file:
        total_size_2 = 0
        for line in file:
            total_size_2 += 1

    with open(file_3) as file:
        total_size_3 = 0
        for line in file:
            total_size_3 += 1

    spirit_1 = eval_data(task, file_1)
    cp_1 = {key: (count / total_size_1) for key, count in spirit_1.items()}

    spirit_2 = eval_data(task, file_2)
    cp_2 = {key: (count / total_size_2) for key, count in spirit_2.items()}

    spirit_3 = eval_data(task, file_3)
    cp_3 = {key: (count / total_size_3) for key, count in spirit_3.items()}

    all_dicts = [ cp_1, cp_2, cp_3 ]

    # Create dictionaries to store the mean and standard deviation for each key
    mean_dict = {}
    std_dict = {}

    # Iterate over the keys
    for key in cp_1.keys():
        # Extract values for the current key from all dictionaries
        values = [ d[ key ] for d in all_dicts ]

        # Calculate mean and standard deviation using numpy
        mean_value = np.mean(values)
        std_value = np.std(values)

        # Store the results in the respective dictionaries
        mean_dict[ key ] = mean_value
        std_dict[ key ] = std_value

    # Print the results
    print("Mean values:", mean_dict)
    print("Standard deviation values:", std_dict)


def main():
    # hate
    print('HATE')
    print('Spiritual')
    calculate_mean_std('predictions_zero_shot/spirituality', 'hate')
    print('Religious')
    calculate_mean_std('predictions_zero_shot/religion', 'hate')

    # emotion
    print('\nEMOTION')
    print('Spiritual')
    calculate_mean_std('predictions_zero_shot/spirituality', 'emotion')
    print('Religious')
    calculate_mean_std('predictions_zero_shot/religion', 'emotion')

    # sentiment
    print('\nSENTIMENT')
    print('Spiritual')
    calculate_mean_std('predictions_zero_shot/spirituality', 'sentiment')
    print('Religious')
    calculate_mean_std('predictions_zero_shot/religion', 'sentiment')

    print('\nOFFENSIVE')
    print('Spiritual')
    calculate_mean_std('predictions_zero_shot/spirituality', 'offensive')
    print('Religious')
    calculate_mean_std('predictions_zero_shot/religion', 'offensive')

    '''
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
    
    '''


if __name__ == '__main__':
    main()
