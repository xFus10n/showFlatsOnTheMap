import pathlib
import pandas as pd
import warnings

import utilz.functions
from utilz import functions as f
from termcolor import colored as c
from datetime import datetime
from utilz import sources as src

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.precision', 10)


def main(mode=None):
    # global mode

    if __name__ == '__main__':
        option_key, options = f.mode_select(src.linkz, 'Choose flats or houses : ')
        mode = options.get(option_key)
        address_in = pathlib.Path('..')
        address_out = pathlib.Path('..')
    else:
        address_in = pathlib.Path('.')
        address_out = pathlib.Path('.')

    address_in_x = address_in.absolute() / 'files/raw' / mode
    address_out_x = address_out.absolute() / 'files/clean' / mode

    date_now = datetime.now().strftime("%Y%m%d%H%M%S")
    warnings.simplefilter(action='ignore', category=FutureWarning)
    staging_exists = address_in.exists() and address_out.exists()
    if staging_exists:
        print(c("staging folders found :", "yellow"), c(str(f.bool_2_human(staging_exists)), "green"))
    else:
        print(c("staging folders found :", "yellow"), c(str(f.bool_2_human(staging_exists)), "red"))
        print(c("system shutdown", "red"))
        exit(1)
    if len(list(address_in_x.glob("**/*.csv"))) == 0:
        print(c('Input folder is empty, run load_ss_lv.py script first', 'red'))
        exit(0)
    # log counts and clear drop zone
    previous_data = f.get_first_file(address_out_x)
    if previous_data != '':
        print(c("unique rows before upload: ", "green"),
              c(str(len(pd.read_csv(previous_data, header=0, sep=';'))), "yellow"))
        f.clear_dir(address_out_x)
    else:
        print(c("unique rows before upload: ", "green"), c(str(0), "yellow"))
    df_full = f.get_csv_files(address_in_x)
    df_full.drop_duplicates(inplace=True, ignore_index=True)

    for transform in utilz.functions.transformation_dispatcher.get(mode):
        df_full = transform(df_full)

    print(c("unique rows after upload: ", "green"), c(str(len(df_full)), "yellow"))
    f.save_as_csv(df_full, address_out_x / f'{date_now}.csv', verbose=True)
    # print(df_full[:1000])
    # exit(0)


if __name__ == "__main__":
    main()
