import pathlib
from datetime import datetime
from utilz import functions as f
from utilz import sources as src
from termcolor import colored as c

global use_proxy


def main():
    global use_proxy

    count = f.how_many_pages_2_download("enter the number of pages to load: ")
    links = src.get_links_for_flats()
    enumerated_keys = src.enumerate_keys(links)
    src.print_dictionary(enumerated_keys)
    city_key = int(input(c('Choose city / region : ', 'green')))
    if city_key != 0:
        address = links.get(enumerated_keys.get(city_key))
        run(address, use_proxy)
    else:
        for region, link in links.items():
            if link != '':
                run(link, count, use_proxy, all_regions=True, postfix=region)


def run(address_0, page_count, use_proxy, all_regions=False, postfix=''):

    # starting page
    page = 1
    # user input
    if not all_regions:
        file_name = str(input("enter file name without extension (leave empty for datetime): "))

    # set path correctly
    if __name__ == '__main__':
        use_proxy = f.needs_proxy()
        location_out = pathlib.Path('..').absolute() / 'files/raw'
    else:
        location_out = pathlib.Path('.').absolute() / 'files/raw'

    # use datetime as name if empty
    date_now = datetime.now().strftime("%Y%m%d%H%M%S")
    if all_regions:
        file_name = date_now + f"_{postfix}"
    else:
        if file_name == '': file_name = date_now

    if location_out.exists():
        print(c("staging folder founded :", "yellow"), c(str(f.bool_2_human(location_out.exists())), "green"))
    else:
        print(c("staging folder found :", "yellow"), c(str(f.bool_2_human(location_out.exists())), "red"))
        print(c("system shutdown", "red"))
        exit(1)
    # will exit after the last page
    df_list = []
    output = location_out / f'{file_name}.csv'
    while True:
        address = f"{address_0}page{page}.html"
        status, data = f.load_page(address, page, proxy=use_proxy)
        if status != 0:
            df_list.append(data)
            if page < page_count:
                page += 1
            else:  # reached the end of requested pages
                break
        else:  # reached the end of pages
            break
    f.list_of_df_to_csv(df_list, output)
    print(c(f"\nSaved {file_name}.csv successfully", "blue"))


if __name__ == "__main__":
    main()
