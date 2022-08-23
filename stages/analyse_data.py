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

# get path to our cleaned file
if __name__ == '__main__':
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
# f.clear_dir(address_out)
df_full = pd.read_csv(file, header=0, sep=';')

# for selling objects in Riga
df_sell = df_full.query("com_type=='sell'")
df_sell = df_sell.groupby(['city', 'region', 'house_type'])['price_m2'].agg(mean='mean', count='count').sort_values(by='mean', ascending=False)
print(df_sell[:100])
print(type(df_full))
print('------------')

# join data
df_full = df_full.join(df_sell, ['city', 'region', 'house_type'])
print(df_full[:100])