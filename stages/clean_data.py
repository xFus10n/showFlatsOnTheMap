import pathlib
import pandas as pd
import warnings

from utilz import functions as f
from termcolor import colored as c
from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.precision', 10)


def main():
    if __name__ == '__main__':
        address_in = pathlib.Path('..').absolute() / 'files/raw'
        address_out = pathlib.Path('..').absolute() / 'files/clean'
    else:
        address_in = pathlib.Path('.').absolute() / 'files/raw'
        address_out = pathlib.Path('.').absolute() / 'files/clean'

    date_now = datetime.now().strftime("%Y%m%d%H%M%S")
    warnings.simplefilter(action='ignore', category=FutureWarning)
    staging_exists = address_in.exists() and address_out.exists()
    if staging_exists:
        print(c("staging folders found :", "yellow"), c(str(f.bool_2_human(staging_exists)), "green"))
    else:
        print(c("staging folders found :", "yellow"), c(str(f.bool_2_human(staging_exists)), "red"))
        print(c("system shutdown", "red"))
        exit(1)
    if len(list(address_in.glob("./*.csv"))) == 0:
        print(c('Input folder is empty, run load_ss_lv.py script first', 'red'))
        exit(0)
    # log counts and clear drop zone
    previous_data = f.get_first_file(address_out)
    if previous_data != '':
        print(c("unique rows before upload: ", "green"),
              c(str(len(pd.read_csv(previous_data, header=0, sep=';'))), "yellow"))
        f.clear_dir(address_out)
    else:
        print(c("unique rows before upload: ", "green"), c(str(0), "yellow"))
    df_full = f.get_csv_files(address_in)
    # print(df_full)
    # exit(0)
    df_full.drop_duplicates(inplace=True, ignore_index=True)
    df_full = f.split_street(df_full)
    df_full = f.split_floor(df_full)
    # price fix
    df_full['price_2'] = df_full.price.str.replace("€", "")  # fixme: na=False
    df_full['price_2'] = df_full.price_2.str.replace("/mēn.", "")
    df_full['price_2'] = df_full.price_2.str.replace("/dienā", "")
    df_full['price_2'] = df_full.price_2.str.replace("maiņai", "")
    df_full['price_2'] = df_full.price_2.str.replace(",", "")
    df_full = f.convert_2_num(df_full, ['rooms', 'floor', 'top_floor', 'm2', 'price_2'])
    # price categorisation
    df_full.loc[df_full['price'].str.contains("€"), 'com_type'] = 'sell'
    df_full.loc[df_full['price'].str.contains("€/mēn"), 'com_type'] = 'rent'
    df_full.loc[df_full['price'].str.contains("€/dienā"), 'com_type'] = 'rent_by_day'
    df_full.loc[df_full['price'].str.contains("vēlosīret"), 'com_type'] = 'want_2_rent'
    df_full.loc[df_full['price'].str.contains("pērku"), 'com_type'] = 'buy'
    df_full.loc[df_full['price'].str.contains('maiņai'), 'com_type'] = 'change'
    print(c("unique rows after upload: ", "green"), c(str(len(df_full)), "yellow"))
    f.save_as_csv(df_full, address_out / f'{date_now}.csv', verbose=True)
    # print(df_full)


if __name__ == "__main__":
    main()
