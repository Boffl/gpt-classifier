import csv
from argparse import ArgumentParser


def reformat_mapping(data_dir):
    classes = []
    file = f'{data_dir}/mapping.txt'
    with open(file, newline='') as csv_file:
        mapping = csv.reader(csv_file, delimiter='\t')
        for row in mapping:
            classes.append(row[0])

    with open(f'{data_dir}/classes_pe.txt', 'w', encoding='utf-8') as writer:
        for cl in classes:
            writer.write(f'{cl}\n')



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('data_dir', help="directory of dataset")
    args = parser.parse_args()

    reformat_mapping(f'{args.data_dir}')