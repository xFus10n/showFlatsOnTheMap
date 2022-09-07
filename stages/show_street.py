import pathlib
import utilz.functions as f
import utilz.aggregations as agg
import pandas as pd
from termcolor import colored as c
from utilz import sources as src

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def main():
    global mode

    # get path to our cleaned file
    if __name__ == '__main__':
        option_key, options = f.mode_select(src.linkz, 'Choose flats or houses : ')
        mode = options.get(option_key)

        address_font = pathlib.Path('.').resolve().parents[0] / 'fonts/arial.ttf'
        address_in = pathlib.Path('.').resolve().parents[0] / 'files/clean' / mode
        address_out = pathlib.Path('.').resolve().parents[0] / 'files/analytical'
    else:
        address_font = pathlib.Path('.').absolute() / 'fonts/arial.ttf'
        address_in = pathlib.Path('.').absolute() / 'files/clean' / mode
        address_out = pathlib.Path('.').absolute() / 'files/analytical'

    staging_exists = address_in.exists() and address_out.exists()
    f.check_staging(staging_exists)
    file = f.get_first_file(address_in)
    if file == '':
        print(c('Input folder is empty, run clean_data.py script first', 'red'))
        exit(0)
    f.clear_dir(address_out)
    pdf = f.create_pdf(address_font)
    columns_flats = ['link', 'street', 'rooms', 'm2', 'house_type', 'price_2', 'price_m2', 'mean', 'flux', 'weight', 'com_type', 'date', 'color', 'lat', 'long']
    columns_houses = ['link', 'street', 'rooms', 'm2', 'out_m2', 'price_2', 'price_m2', 'mean', 'flux', 'weight', 'com_type', 'date', 'color', 'lat', 'long']
    columnz = columns_flats if mode == 'flats' else columns_houses
    df_full = pd.read_csv(file, header=0, sep=';')

    # ask for city
    df_cities = df_full['city'].drop_duplicates().reset_index(drop=True)
    print(df_cities)
    position = input(c(f"Choose city: ", "green"))
    key_city = df_cities.iloc[[position]].tolist()[0]
    df_full = df_full.query(f'city == "{key_city}"')

    # ask for region input
    df_out, regions = agg.get_streets_short(df_full)
    print(regions)
    position = input(c(f"Choose region: ", "green"))
    key_reg = regions.iloc[[position]].tolist()[0]
    df_reg = df_out.query(f'region == "{key_reg}"')

    # ask for street
    df_street = pd.crosstab(df_reg.street_short, df_reg.color).reset_index()
    df_street.index.names = ['index']
    print(df_street)

    position = input(c(f"Choose street ", "green") + c("(empty = all)", "blue") + c(" : ", "green"))
    position = int(position) if position.isdigit() else None

    # show results
    if position is None:
        df = df_reg
    else:
        key = df_street['street_short'].iloc[[position]].tolist()[0]
        df = df_reg.query(f'street_short == "{key}"')
    f.log_dataframe_with_geo_data(df[columnz], address_out, str(key_reg).upper(), 'show_map', pdf, mode, new_page=True)
    pdf.output(address_out / 'data.pdf')


if __name__ == "__main__":
    main()
