import pathlib
from datetime import datetime
from utilz import functions as f
from utilz import sources as src
from termcolor import colored as c

global use_proxy


def main():
    global use_proxy
    use_proxy = f.needs_proxy() if __name__ == '__main__' else use_proxy
    count = f.how_many_pages_2_download("enter the number of pages to load: ")
    links = src.get_links_for_flats()
    enumerated_keys = src.enumerate_keys(links)
    src.print_dictionary(enumerated_keys)
    city_key = int(input(c('Choose city / region : ', 'green')))
    if city_key != 0:
        region = enumerated_keys.get(city_key)
        address = links.get(region)
        run(address, count, use_proxy, filename=region)
    else:
        for region, link in links.items():
            if link != '':
                run(link, count, use_proxy, filename=region)


def run(address_0, page_count, use_proxy, filename=''):

    # starting page
    page = 1

    # set path correctly
    if __name__ == '__main__':
        location_out = pathlib.Path('..').absolute() / 'files/raw'
    else:
        location_out = pathlib.Path('.').absolute() / 'files/raw'

    # use datetime as name if empty
    date_now = datetime.now().strftime("%Y%m%d")

    if location_out.exists():
        print(c("staging folder founded :", "yellow"), c(str(f.bool_2_human(location_out.exists())), "green"))
    else:
        print(c("staging folder found :", "yellow"), c(str(f.bool_2_human(location_out.exists())), "red"))
        print(c("system shutdown", "red"))
        exit(1)
    # will exit after the last page
    df_list = []
    output = location_out / f'{date_now}/{filename}.csv'
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
    print(c(f"\nSaved {filename}.csv successfully", "blue"))


if __name__ == "__main__":
    main()
