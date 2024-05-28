### Riga flats statistics using data from ss.lv
This is a simple data pipeline for Flats analysis.
Project is written in a python and data source was ss.lv

### Installation

Pyrthon version: 3.11.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 
all required libraries. Assuming, *readme.md* location is
current active directory. Then command to install dependencies:

```bash
pip install -r requirements.txt
```

If current active directory is different, then, please specify
path to *requirements.txt*

```bash
pip install -r .\some_folder\requirements.txt
```

## Usage
There are 3 folders under **files** directory:
* **raw** - contains source files
* **clean** - contains cleaned/transformed so2urce files
* **analytical** - contains output files

These folders being used for data processing.

**NOTE: Scripts location and folder structure should be preserved** 

**NOTE: If your connection is under proxy, re-implement *utilz.functions.get_proxies* function** 

* ###Load
  For data download run [load](stages/load_ss_lv.py) script.
  User can specify a file name, number of pages to download and either the connection is under proxy.
  Proxies can be specified in here : **./utilz/functions.get_proxies**. Multiple
  files allowed (deduplication happens on the next stage). If number of pages are less than user have specified, script will stop 
  downloading at the last available page.
* ###Clean/Transform
  For data cleansing/transforming run [clean](stages/clean_data.py) script.
  Output folder will be erased before saving new file.
* ###Analyse
  For data analysis run [analyse](stages/analyse_data.py) script. Will be asked either your internet 
  connection requires proxy and wether you wan to pop up the plots. The output files will be
  saved in *analytical* folder. The folder will be cleared prior saving. Summary can be found in 
  *data.pdf* file. NOTE: There are clickable areas on the pdf for maps pop-up (*top_10_sell_map, top_10_rent_map, top_10_rent_day_map*)
* ###main
  Runs all stages