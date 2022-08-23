import pandas as pd
import numpy as np


def most_expensive(df_full, columns, com_type):
    df = df_full[columns].query(f"com_type == '{com_type}'")
    return df.groupby(['region'])['price_2'].max().to_frame().sort_values('price_2', ascending=False)


def average_price(df_full, columns, com_type):
    df = df_full[columns].query(f"com_type == '{com_type}'")
    return df.groupby(['region'])['price_2'].mean().round(0).to_frame().sort_values('price_2', ascending=False)


def max_top_n(df_full, columns, com_type, n):
    df_max = df_full.query(f"com_type == '{com_type}'")
    return df_max[columns].sort_values('price_2', ascending=False).head(n)


def get_top_zones(df_full):
    df_com = df_full[['region']] \
        .groupby('region') \
        .agg(counts=pd.NamedAgg(column='region', aggfunc='count')) \
        .sort_values('counts', ascending=False)
    df_com.insert(0, 'zone', df_com.index)
    df_filter = df_com['counts'] > 100
    df_com = df_com[df_filter]
    return df_com, df_com['zone'].tolist()


def get_streets_short(df_full):
    # drop values with no street data
    df_filter = df_full[df_full['street'].notna()].copy()

    # split street
    df_filter['street_list'] = df_filter['street'].str.lower().str.replace(r'\d+.', '', regex=True).str.split(' ')

    # check whether first part contains more than 3 symbols
    df_filter['first_part_valid'] = np.where(df_filter['street_list'].str[0].str.len() > 3, True, False)

    # set grouping street column
    df_filter['street_short'] = np.where(df_filter.first_part_valid, df_filter.street_list.str[0],
                                         df_filter.street_list.str[1])

    # cast to string
    df_filter[['region', 'street_short']] = df_filter[['region', 'street_short']].astype('string')

    # get short streets
    region = df_filter['region'].drop_duplicates().sort_values(ascending=True).reset_index(drop=True)

    # region_streets = region_streets.groupby('region')['street_short'].apply(list).to_frame()
    return df_filter, region


def get_house_types_by_zones(df_reduced):
    df_com = df_reduced[['region', 'house_type']] \
        .replace({'house_type': {"-": "Unspecified"}}) \
        .groupby(['region', 'house_type']) \
        .agg(counts=pd.NamedAgg(column='house_type', aggfunc='count')) \
        .sort_values(['region', 'counts'], ascending=False)
    return df_com.reset_index()


def commercials_for_category(df_full):
    df_com = df_full[['com_type']] \
        .groupby('com_type') \
        .agg(counts=pd.NamedAgg(column='com_type', aggfunc='count')) \
        .sort_values('counts', ascending=False)
    df_com.insert(0, 'com_type_col', df_com.index)
    return df_com


def commercials_for_house_type(df_full):
    df_com = df_full[['house_type']] \
        .replace({'house_type': {"-": "Unspecified"}}) \
        .groupby('house_type') \
        .agg(counts=pd.NamedAgg(column='house_type', aggfunc='count')) \
        .sort_values('counts', ascending=False)
    df_com.insert(0, 'house_type_col', df_com.index)
    return df_com
