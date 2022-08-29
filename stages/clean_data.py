import pathlib
import pandas as pd
import warnings

from utilz import functions as f
from termcolor import colored as c
from datetime import datetime
from utilz.aggregations import mean_selling_price as mp

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
    if len(list(address_in.glob("**/*.csv"))) == 0:
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
    df_full.drop_duplicates(inplace=True, ignore_index=True)
    df_full = f.refine_date(df_full)
    df_full = f.check_city(df_full)
    df_full = f.set_date_color(df_full)
    df_full = f.split_floor(df_full)

    # price fix
    df_full = f.split_price(df_full)
    df_full['price_m2'] = df_full.price_m2.str.replace("€/m²\\)", "")
    df_full['price_m2'] = df_full.price_m2.str.replace(" ", "")
    df_full['price_m2'] = df_full.price_m2.fillna('nan')

    df_full['price'] = df_full['price'].fillna('nan')
    df_full['price_2'] = df_full.price.str.replace("€", "")
    df_full['price_2'] = df_full.price_2.str.replace("/mēn.", "")
    df_full['price_2'] = df_full.price_2.str.replace("/dienā", "")
    df_full['price_2'] = df_full.price_2.str.replace("maiņai", "")
    df_full['price_2'] = df_full.price_2.str.replace(",", "")
    df_full['price_2'] = df_full.price_2.str.replace(" ", "")
    df_full = f.convert_2_num(df_full, ['rooms', 'floor', 'top_floor', 'm2', 'price_2', 'price_m2', 'lat', 'long'])

    # price categorisation
    df_full.loc[df_full['price'].str.contains('nan'), 'com_type'] = 'other'
    df_full.loc[df_full['price'].str.contains("€"), 'com_type'] = 'sell'
    df_full.loc[df_full['price'].str.contains("€/mēn"), 'com_type'] = 'rent'
    df_full.loc[df_full['price'].str.contains("€/dienā"), 'com_type'] = 'rent_by_day'
    df_full.loc[df_full['price'].str.contains("vēlosīret"), 'com_type'] = 'want_2_rent'
    df_full.loc[df_full['price'].str.contains("pērku"), 'com_type'] = 'buy'
    df_full.loc[df_full['price'].str.contains('maiņai'), 'com_type'] = 'change'

    # mean price for region /house type & round up
    df_full = mp(df_full)
    df_full[['mean', 'weight', 'rooms', 'm2', 'flux', 'price_2', 'price_m2']] = df_full[['mean', 'weight', 'rooms', 'm2', 'flux', 'price_2', 'price_m2']].fillna(0)
    df_full[['mean', 'weight', 'rooms', 'm2', 'price_2', 'price_m2']] = df_full[['mean', 'weight', 'rooms', 'm2', 'price_2', 'price_m2']].round(0).astype(int)
    df_full['flux'] = df_full['flux'].round(2)

    print(c("unique rows after upload: ", "green"), c(str(len(df_full)), "yellow"))
    f.save_as_csv(df_full, address_out / f'{date_now}.csv', verbose=True)
    # print(df_full[:1000])
    # exit(0)


if __name__ == "__main__":
    main()
