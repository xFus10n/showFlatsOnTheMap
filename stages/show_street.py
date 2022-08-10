import pathlib
import utilz.functions as f
import utilz.aggregations as agg
import pandas as pd
import kaleido
from termcolor import colored as c

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def main():
    global use_proxy

    # get path to our cleaned file
    if __name__ == '__main__':
        use_proxy = f.needs_proxy()
        address_font = pathlib.Path('.').resolve().parents[0] / 'fonts/arial.ttf'
        address_in = pathlib.Path('.').resolve().parents[0] / 'files/clean'
        address_out = pathlib.Path('.').resolve().parents[0] / 'files/analytical'
    else:
        address_font = pathlib.Path('.').absolute() / 'fonts/arial.ttf'
        address_in = pathlib.Path('.').absolute() / 'files/clean'
        address_out = pathlib.Path('.').absolute() / 'files/analytical'

    file = f.get_first_file(address_in)
    staging_exists = address_in.exists() and address_out.exists()
    f.check_staging(staging_exists)
    if file == '':
        print(c('Input folder is empty, run clean_data.py script first', 'red'))
        exit(0)
    f.clear_dir(address_out)
    pdf = f.create_pdf(address_font)
    columnz = ['link', 'street', 'rooms', 'floor', 'm2', 'house_type', 'price_2', 'com_type']
    df_full = pd.read_csv(file, header=0, sep=';')
    df_out, regions = agg.get_streets_short(df_full)
    # ask for region input
    print(regions)
    position = input(c(f"Choose region: ", "green"))
    key_reg = regions.iloc[[position]].tolist()[0]
    df_reg = df_out.query(f'region == "{key_reg}"')
    # print(df_reg)
    # ask for street
    # df_street = df_reg['street_short'].drop_duplicates().sort_values(ascending=True).reset_index(drop=True)
    df_street = df_reg.groupby(['street_short'])\
        .agg(count=pd.NamedAgg(column="street_short", aggfunc="count")).reset_index()
    print(df_street)
    try:
        position = int(input(c(f"Choose street ", "green") + c("(empty = all)", "blue") + c(" : ", "green")))
    except ValueError as ve:
        position = None
    # show results
    if position is None:
        df = df_reg
    else:
        key = df_street['street_short'].iloc[[position]].tolist()[0]
        df = df_reg.query(f'street_short == "{key}"')
    # get geo data
    df_geo = f.get_geo_data(df[columnz], use_proxy=use_proxy)
    f.log_dataframe_with_geo_data(df_geo, address_out, str(key_reg).upper(), 'show_map', pdf, new_page=True)
    pdf.output(address_out / 'data.pdf')


if __name__ == "__main__":
    main()
