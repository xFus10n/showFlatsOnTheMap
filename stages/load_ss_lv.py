import pathlib
from datetime import datetime
from utilz import functions as f
from utilz import sources as src
from termcolor import colored as c


def main():
    global use_proxy

    # user inputs
    option_key, options = mode_select(src.linkz, 'Choose flats or houses : ')
    use_proxy = f.needs_proxy() if __name__ == '__main__' else use_proxy
    page_count = f.how_many_pages_2_download("enter the number of pages to load: ")

    links = src.get_links(options.get(option_key))
    city_key, city_options = mode_select(links, 'Choose city / region : ')  # user input

    if city_key != 0:  # 0 -> all
        address = links.get(city_options.get(city_key))
        run(address, page_count, use_proxy, filename=city_options.get(city_key))
    else:
        for region, link in links.items():
            if link != '':
                run(link, page_count, use_proxy, filename=region)


def mode_select(dictionary, msg):
    options = src.enumerate_keys(dictionary)  # flats or houses
    src.print_dictionary(options)
    option_key = int(input(c(msg, 'green')))
    return option_key, options


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
