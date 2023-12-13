import pandas as pd
import csv




def subsample_month(df):
    overall_subsample = pd.DataFrame()

    # Iterate over unique months
    for month in set(df[ 'month' ]):
        # Subsample based on the number of entries for the current month
        month_subsample = df[ df[ 'month' ] == month ].sample(frac=0.01,
                                                              random_state=58)  # Adjust the fraction as needed
        overall_subsample = pd.concat([ overall_subsample, month_subsample ], ignore_index=True)

    return overall_subsample


def get_month_dist(df):
    df[ 'month' ] = df[ 'month' ].astype(int)

    # Count the occurrences of each month
    month_distribution = df[ 'month' ].value_counts().sort_index()

    return month_distribution


def spiritual_religious_df(df):
    # filter cases where both religious and spiritual occur

    df_religion = df[ df[ 'religion' ] == True ]
    df_spirit = df[ df[ 'spirituality' ] == True ]

    df_rel_spirit = df[ (df[ 'spirituality' ] == True) & (df[ 'religion' ] == True) ]

    df_religion = pd.concat([ df_religion, df_rel_spirit, df_rel_spirit ]).drop_duplicates(keep=False)
    df_spirit = pd.concat([ df_spirit, df_rel_spirit, df_rel_spirit ]).drop_duplicates(keep=False)

    return df_spirit['clean_text'], df_religion['clean_text']


def write_csv(df, task):

    file_map = {'r': 'religious_text_001_3.txt', 's': 'spiritual_text001_3".txt'}
    with open(file_map[task], 'w', encoding='utf-8') as file:
        data_list = df.values.tolist()
        for line in data_list:
            file.write(f'{line}\n')





def main():
    df = pd.read_csv('full_year.csv')
    subsample = subsample_month(df)
    print(get_month_dist(df))
    df_spirit, df_religion = spiritual_religious_df(subsample)
    write_csv(df_spirit, 's')
    write_csv(df_religion, 'r')


if __name__ == "__main__":
    main()
