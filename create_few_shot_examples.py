from argparse import ArgumentParser
import os
from encode_predictions import get_mapping
import random
import jsonlines



# Todo: make a stratified sample of the training data
# for each class the same amount of examples, for a total of n examples
# use the validation set

# read in the two files, create two lists

# find out how many classes there are

# make a list of tuples (class, tweet) for each of the classes

# make a random sample with the indices where k = n/|classes|

# write into the jsonl

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('task', choices=['emotion', 'hate', 'offensive', 'sentiment'])
    parser.add_argument('shots', type=int, help='how many shots? Has to be an even number.')
    parser.add_argument('--data_dir', default='raw_data')
    args = parser.parse_args()
    data_dir = args.data_dir
    shots = int(args.shots)
    task = args.task

    # get the mapping:
    mapping = get_mapping(os.path.join(data_dir, task, 'mapping.txt'))
    # have to reverse the mapping, bc we wanna decode
    mapping = {v: k for k, v in mapping.items()}

    # read in the label and text files, create two lists
    filepath_labels = os.path.join(data_dir, task, 'val_labels.txt')
    filepath_texts = os.path.join(data_dir, task, 'val_text.txt')
    val_labels = []
    val_texts= []
    with open(filepath_labels, 'r', encoding='utf-8') as label_file, open(filepath_texts, 'r', encoding='utf-8') as text_file:
        for val_label, val_text in zip(label_file, text_file):
            label = mapping[val_label.strip()]
            val_labels.append(label)
            val_texts.append(val_text.strip())

    # find out how many classes there are
    n_classes = len(set(val_labels))
    # check if the number of shots is a multiple of the number of classes
    if shots % n_classes:
        print("Number of shots must be a multiple of the number of classes...")
        exit(1)
    # sample size for each of the classes
    sample_size = int(shots / n_classes)

    # make a list of lists, with each a list for each classs with of tuples with (label, text)
    # the indexes of the list are [class][examples]
    big_list = []
    for label in set(val_labels):
        # indices of the elements with the class
        indices = [i for i, x in enumerate(val_labels) if x == label]
        # sample
        sample_indices = random.sample(indices, sample_size)

        tuple_list = [(val_labels[i], val_texts[i]) for i in sample_indices]
        big_list += tuple_list

    # shuffle the examples, so the model does not memorize a pattern
    random.shuffle(big_list)
    write_example_list = []
    for label, text in big_list:
        # write the json lines
        write_example_list.append({"role": "user", "content": text})
        write_example_list.append({"role": "assistant", "content": label})


    example_filepath = os.path.join(data_dir, task, 'examples.jsonl')
    with jsonlines.open(example_filepath, 'w') as jsonl_file:
        jsonl_file.write_all(write_example_list)









