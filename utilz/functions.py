import pathlib
import string

import numpy
import pandas
import folium
import requests as req
import bs4
import os
from termcolor import colored as c
import fpdf
import plotly.express as px
import time

from utilz.PageAttributes import get_city, get_region, get_street, get_rooms, get_area_m2, get_floor, get_house_type, \
    get_price, get_date, get_location, get_house_rooms, get_outer_area_m2, get_floor_count, get_amenities
from utilz.aggregations import mean_selling_price, find_price_for_m2
from utilz.sources import columnz, linkz, flats, houses


def plot_barchart(data_frame, x_axis, y_axis, path_out, f_name, p_name, pdf, labels, show_fig=False):
    path = str(path_out / f'{f_name}.png')
    fig = px.bar(data_frame, x=x_axis, y=y_axis, text=y_axis, labels=labels)
    fig.update_traces(textposition=['auto'])  # ['inside', 'outside', 'auto', 'none']
    fig.update_layout(

        title_text=p_name
    )
    if show_fig: fig.show()
    fig.write_image(path_out / f'{f_name}.png')
    pdf.image(path, w=pdf.w - 2 * pdf.l_margin, h=pdf.h / 2.5)


def plot_barchart_v2(data_frame, x_axis, y_axis, y_color, path_out, f_name, p_name, pdf, show_fig=False):
    path = str(path_out / f'{f_name}.png')
    fig = px.bar(data_frame, x=x_axis, y=y_axis, color=y_color, text_auto=True, orientation='v')
    fig.update_layout(

        title_text=p_name
    )
    if show_fig: fig.show()
    fig.write_image(path_out / f'{f_name}.png')
    pdf.image(path, w=pdf.w - 2 * pdf.l_margin, h=pdf.h - 2 * pdf.t_margin)


def log_dataframe(data_frame, caption, select_columns, pdf, new_page=False):
    add_item_to_pdf(pdf, caption, 40, 10, new_page=new_page)  # Caption
    log_data_pdf(pdf, data_frame[select_columns])
    # add_item_to_pdf(pdf, '', 40, 10, new_page=new_page)  # Space


def log_dataframe_with_geo_data(data_frame, out_path, caption, html_name, pdf, mode, new_page=False):
    q_path = create_map_html(data_frame, str(out_path), html_name, mode)
    add_item_to_pdf(pdf, caption, 40, 10, new_page=new_page)  # Caption
    log_data_pdf(pdf, drop_col(data_frame, ['lat', 'long']))
    add_item_to_pdf(pdf, q_path, 20, 10, is_link=True, link_msg=html_name)  # link to map


def check_staging(both_exist):
    if both_exist:
        print(c("staging folders found :", "yellow"), c(str(bool_2_human(both_exist)), "green"))
    else:
        print(c("staging folders found :", "yellow"), c(str(bool_2_human(both_exist)), "red"))
        print(c("system shutdown", "red"))
        exit(1)


def create_pdf():
    pdf = fpdf.FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('Arial', '', '../fonts/arial.ttf', uni=True)
    pdf.set_font('Arial', '', 10)
    return pdf


def create_pdf(address_font):
    pdf = fpdf.FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('Arial', '', address_font, uni=True)
    pdf.set_font('Arial', '', 9)
    return pdf


def log_data_pdf(pdf, data_frame):
    short_col_factor = 1.8  # div
    long_col_factor = 2.1   # mult
    short_cols = ('rooms', 'floor', 'm2', 'weight', 'flux')
    long_cols = ('street', 'date')
    omit_columns = ('link', 'color')
    real_width = pdf.w - 2 * pdf.l_margin
    column_width = real_width / len(data_frame.columns)
    row_hight = pdf.font_size * 2

    # header
    for col in data_frame.columns:
        if col in omit_columns:
            pass
        elif col in short_cols:
            pdf.cell(column_width / short_col_factor, row_hight, str(col), border=1, align='C')
        elif col in long_cols:
            pdf.cell(column_width * long_col_factor, row_hight, str(col), border=1, align='C')
        else:
            pdf.cell(column_width, row_hight, str(col), border=1, align='C')
    pdf.ln()

    # data
    for i in range(data_frame.shape[0]):
        for col in data_frame.columns:
            if col in omit_columns:
                pass
            elif col in short_cols:
                pdf.cell(column_width / short_col_factor, row_hight, str(data_frame[col].iloc[i]), border=1)
            elif col in long_cols:
                pdf.cell(column_width * long_col_factor, row_hight, str(data_frame[col].iloc[i]), border=1)
            else:
                pdf.cell(column_width, row_hight, str(data_frame[col].iloc[i]), border=1)
        pdf.ln()


def add_item_to_pdf(pdf, item, width, hight, new_page=False, is_link=False, link_msg=''):
    if new_page:
        pdf.add_page()
    if is_link:
        pdf.cell(width, hight, link_msg, border=0, ln=0, align='', fill=False, link=item)
    else:
        pdf.cell(width, hight, item, border=0, ln=0, align='', fill=False)
    pdf.ln()
    return pdf


def get_proxies():
    return {
        'http': 'http://proxy.lvrix.atrema.deloitte.com:3128',
        'https': 'http://proxy.lvrix.atrema.deloitte.com:3128',
    }


def create_map_html(data_frame, path_2_analytical_dir, name, mode):
    full_html_name = ''
    data_frame_clear = data_frame.dropna()
    if len(data_frame_clear) == 0:
        print(c("error deleting NaNs", "red"))
        exit(1)
    df = data_frame_clear.copy()
    df['info'] = build_msg_popup(df, mode)
    try:
        mapx = folium.Map(location=[df.lat.mean(), df.long.mean()], zoom_start=14, control_scale=True)
        for index, location_info in df.iterrows():
            iframe = folium.IFrame(location_info['info'])
            popup = folium.Popup(iframe, min_width=300, max_width=300)
            folium.Marker([location_info["lat"], location_info["long"]],
                          popup=popup, icon=folium.Icon(color=location_info['color'])).add_to(mapx)
        full_html_name = f"{path_2_analytical_dir}/{name}.html"
        mapx.save(full_html_name)
    except AttributeError as e:
        print(e)
        pass
    return full_html_name


def build_msg_popup(df, mode):
    if mode == flats:
        return '<b>Commercial Type:</b> ' + df['com_type'].map(str) + ',<br>' \
               + '<b>Location:</b> ' + df['street'].map(str) + ',<br>' \
               + '<b>Building Type:</b> ' + df['house_type'].map(str) + ',<br>' \
               + '<b>Area:</b> ' + df['m2'].map(str) + '(m2),<br>' \
               + '<b>Price:</b> ' + df['price_2'].map(str) + '(EUR),<br>' \
               + '<b>Flux:</b> ' + df['flux'].map(str) + ',<br>' \
               + '<b>Date:</b> ' + df['date'].map(str) + ',<br>' \
               + '<b>Link:</b> <a href="' + df['link'].map(str) + '" target="_blank">source</a>'
    else:
        return '<b>Commercial Type:</b> ' + df['com_type'].map(str) + ',<br>' \
               + '<b>Location:</b> ' + df['street'].map(str) + ',<br>' \
               + '<b>Area:</b> ' + df['m2'].map(str) + '(m2),<br>' \
               + '<b>Outer Area:</b> ' + df['out_m2'].map(str) + '(m2),<br>' \
               + '<b>Price:</b> ' + df['price_2'].map(str) + '(EUR),<br>' \
               + '<b>Flux:</b> ' + df['flux'].map(str) + ',<br>' \
               + '<b>Date:</b> ' + df['date'].map(str) + ',<br>' \
               + '<b>Link:</b> <a href="' + df['link'].map(str) + '" target="_blank">source</a>'


# def crete_msg_popup(df, columns):
#     output = ""
#     for col in columns:
#         if col in df.columns:
#             output = output + ...


def drop_col(data_frame, columns):
    for col in columns:
        del data_frame[col]
    return data_frame


def how_many_pages_2_download(prompt):
    try:
        count = int(input(prompt))
        if count < 1:
            raise ValueError('cannot download less then 0 pages, returning 1')
    except ValueError as e:
        count = 1
        print(c(str(e), "red"))
    return count


def needs_proxy():
    proxy = str(input('Connect with proxy (y/n) : '))
    return proxy.lower() == 'y'


def download_new_data():
    proxy = str(input('Download new data? (y/n) : '))
    return proxy.lower() == 'y'


def show_charts():
    proxy = str(input('Show charts (y/n) : '))
    return proxy.lower() == 'y'


def get_idz(page_content: bs4.BeautifulSoup):
    out = []
    idz = page_content.find_all("tr", id=True)
    for line in idz:
        try:
            idz = line.attrs['id']
        except KeyError:
            pass
        if len(idz) == 11:
            out.append(idz)
    return out


def show(anything, show_lines=True):
    for each in anything:
        if show_lines:
            print(each, f" items: {len(each)}")
        else:
            print(each)


def write(data_list, name: string):
    with open(name, mode="w", encoding="utf-8") as file:
        for data in data_list:
            for item in data:
                file.write(f"\t{item}")
            file.write("\n")


def create_dataframe(data_list, columns):
    return pandas.DataFrame(data_list, columns=columns)


def update_xcell(data_frame, file_name, sheet_name):
    try:
        with pandas.ExcelWriter(file_name, mode='a', engine='openpyxl') as xl_writer:
            data_frame.to_excel(xl_writer, sheet_name=sheet_name, index=False)
    except FileNotFoundError:
        data_frame.to_excel(file_name, engine='openpyxl', sheet_name=sheet_name, index=False)


def save_as_csv(data_frame, filename, verbose=False):
    filename.parents[0].mkdir(parents=True, exist_ok=True)
    data_frame.to_csv(filename, index=False, encoding='utf8', mode='a', header=True, sep=';')
    if verbose:
        print(c(f"Saved data under ", "blue"), end=" : ")
        print(c(f"{filename.parts[-2]} / {filename.name}", "yellow"))


def list_of_df_to_csv(df_list, filename):
    filename.parents[0].mkdir(parents=True, exist_ok=True)
    pandas.concat(df_list).to_csv(filename, index=False, encoding='utf8', sep=';')


def clear_dir(location):
    for path in list(location.iterdir()):
        os.remove(path)


def get_csv_files(address_in):
    df_list = list()
    for path in list(address_in.glob("**/*.csv")):
        # print(path)
        df_list.append(pandas.read_csv(path, header=0, sep=';'))
    df_full = pandas.concat(df_list, ignore_index=True, sort=False)
    return df_full


def get_first_file(address):
    try:
        clean_zone_first = list(address.glob("./*.csv"))
        return clean_zone_first[0]
    except IndexError:
        return ''


def get_page(addr, use_proxy=False):
    max_retries = 3
    while max_retries != 0:
        try:
            if use_proxy:
                page = req.get(addr, proxies=get_proxies())
            else:
                page = req.get(addr)
            return page
        except Exception as e:
            max_retries = max_retries - 1
            print(c(f"Failed to connect, attempts left: {max_retries}", "red"))
            time.sleep(5)


def load_page(mode, address, page_number, proxy=False):
    # load the page
    page = get_page(address, proxy)

    # check if page are the same, not -> reached end
    if page.url != address:
        print(c("\nReached end of pages   :", "yellow"), c("stopping", "green"))
        return 0, None

    info = []  # info holder

    if page.status_code == 200:
        # print(c(f"connection success", "yellow"), end=c(" => ", "yellow"))
        page_content = bs4.BeautifulSoup(page.content, "html.parser")

        # Get Data
        idz = get_idz(page_content)
        for current_id in idz:
            current_info = []
            table_row = page_content.find(id=current_id)

            # short text
            row_object = table_row.find("a", class_="am")
            if row_object is not None: current_info.append(row_object.string) # short text

            if row_object is not None:
                extracted_link = "https://ss.lv" + row_object.attrs["href"]
                current_info.append(extracted_link)

                internal_page = get_page(extracted_link, proxy)
                if internal_page.status_code == 200:
                    internal_page_content = bs4.BeautifulSoup(internal_page.content, "html.parser")
                    for page_element in elements_dispatcher.get(mode):
                        page_element(current_info, internal_page_content)

            # append data
            info.append(current_info)
    else:
        print(c("Error", "red"))

    # print array
    # show(info, True)
    # exit(0)
    df = create_dataframe(info, columnz.get(mode))

    # print(df)
    print(c(f"\rConnection success     :", "yellow"), c(f"page: {page_number} loaded ...", "green"), end='')
    return 1, df


def refine_date(df):
    df['date'] = df['date'].str.replace('Datums: ', '')
    df['date'] = pandas.to_datetime(df['date'], format='%d.%m.%Y %H:%M')
    return df


def check_city(df):
    df['city'] = df['city'].fillna('unknown')
    return df


def set_date_color(df):
    # current_date = pandas.datetime.now()
    current_date = pandas.Timestamp.now()
    df['date_diff'] = current_date - df['date']
    df['date_diff'] = df['date_diff'] / numpy.timedelta64(1, 'D')
    df.loc[df['date_diff'] <= 1, 'color'] = 'red'
    df.loc[(df['date_diff'] > 1) & (df['date_diff'] <= 2), 'color'] = 'orange'
    df.loc[(df['date_diff'] > 2) & (df['date_diff'] <= 5), 'color'] = 'green'
    df.loc[df['date_diff'] > 5, 'color'] = 'black'
    return df


def split_floor(df):
    df[['floor', 'top_floor']] = df.floor.str.split("/", expand=True)
    return df


def split_price(df):
    df[['price', 'price_m2']] = df.price.str.split("(", expand=True)
    return df


def convert_2_num(data, data_type="float64"):
    columns = ['rooms', 'floor', 'top_floor', 'm2', 'price_2', 'price_m2', 'lat', 'long', 'out_m2']
    for column in columns:
        if column in data.columns:
            data[column] = pandas.to_numeric(data[column], errors="coerce")
            data[column] = data[column].astype(data_type, errors='ignore')
    return data


def bool_2_human(true_or_false):
    if true_or_false:
        return 'Yes'
    else:
        return 'No'


def mode_select(dictionary, msg):
    options = enumerate_keys(dictionary)  # flats or houses
    print_dictionary(options)
    option_key = int(input(c(msg, 'green')))
    return option_key, options


def fix_m2_price(df_full):
    df_full['price_m2'] = df_full.price_m2.str.replace("€/m²\\)", "")
    df_full['price_m2'] = df_full.price_m2.str.replace(" ", "")
    df_full['price_m2'] = df_full.price_m2.fillna('nan')
    return df_full


def refine_price(df_full):
    df_full['price'] = df_full['price'].fillna('nan')
    df_full['price_2'] = df_full.price.str.replace("€", "")
    df_full['price_2'] = df_full.price_2.str.replace("/mēn.", "")
    df_full['price_2'] = df_full.price_2.str.replace("/dienā", "")
    df_full['price_2'] = df_full.price_2.str.replace("maiņai", "")
    df_full['price_2'] = df_full.price_2.str.replace(",", "")
    df_full['price_2'] = df_full.price_2.str.replace(" ", "")
    return df_full


def categorize(df_full):
    df_full.loc[df_full['price'].str.contains('nan'), 'com_type'] = 'other'
    df_full.loc[df_full['price'].str.contains("€"), 'com_type'] = 'sell'
    df_full.loc[df_full['price'].str.contains("€/mēn"), 'com_type'] = 'rent'
    df_full.loc[df_full['price'].str.contains("€/dienā"), 'com_type'] = 'rent_by_day'
    df_full.loc[df_full['price'].str.contains("vēlosīret"), 'com_type'] = 'want_2_rent'
    df_full.loc[df_full['price'].str.contains("pērku"), 'com_type'] = 'buy'
    df_full.loc[df_full['price'].str.contains('maiņai'), 'com_type'] = 'change'
    return df_full


def get_links(key):
    return linkz.get(key)


def enumerate_keys(dictionary):
    sequence = [x for x in range(len(dictionary.keys()))]
    return dict(zip(sequence, dictionary.keys()))


def print_dictionary(dictionary):
    [print(key, ' : ', val) for key, val in dictionary.items()]


def round_cast_int(df_full):
    cols2fillna = ['mean', 'weight', 'rooms', 'm2', 'flux', 'price_2', 'price_m2', 'floor', 'out_m2']
    cols2round_cast_0 = ['mean', 'weight', 'rooms', 'm2', 'price_2', 'price_m2', 'floor', 'out_m2']
    cols2round_cast_2 = ['flux']

    for col in cols2fillna:
        if col in df_full.columns: df_full[col] = df_full[col].fillna(0)

    for col in cols2round_cast_0:
        if col in df_full.columns: df_full[col] = df_full[col].round(0).astype(int)

    for col in cols2round_cast_2:
        if col in df_full.columns: df_full[col] = df_full[col].round(2)

    return df_full


transformation_dispatcher = {flats: [refine_date, check_city, set_date_color, split_floor, split_price, fix_m2_price, refine_price, convert_2_num, categorize, mean_selling_price, round_cast_int],
                             houses: [refine_date, check_city, set_date_color, refine_price, convert_2_num, find_price_for_m2, categorize, mean_selling_price, round_cast_int]}
elements_dispatcher = {
    flats: [get_city, get_region, get_street, get_rooms, get_area_m2, get_floor, get_house_type, get_price, get_date,
            get_location],
    houses: [get_city, get_region, get_street, get_house_rooms, get_outer_area_m2, get_area_m2, get_floor_count,
             get_amenities, get_price, get_date, get_location]}