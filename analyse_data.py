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
address_in = pathlib.Path('.').absolute()/'files/clean'
address_out = pathlib.Path('.').absolute()/'files/analytical'

file = f.get_first_file(address_in)

if __name__ == "__main__":

    staging_exists = address_in.exists() and address_out.exists()
    f.check_staging(staging_exists)
    if file == '':
        print(c('Input folder is empty, run clean_data.py script first', 'red'))
        exit(0)
    f.clear_dir(address_out)

    use_proxy = f.needs_proxy()
    show = f.show_charts()
    df_full = pd.read_csv(file, header=0, sep=';')
    pdf = f.create_pdf()

    # reducing zones
    df_com, zones = agg.get_top_zones(df_full)
    f.log_dataframe(df_com, 'Nuber of commercials in regions (count > 100): ', ['zone', 'counts'], pdf, new_page=True)

    # zone - house types
    caption = "\t\tNuber of commercials in regions grouped by house type: "
    df_reduced = df_full[df_full['region'].isin(zones)]
    df_com = agg.get_house_types_by_zones(df_reduced)
    # f.add_item_to_pdf(pdf, "Nuber of commercials in regions grouped by house type : ", 40, 10)
    f.plot_barchart_v2(df_com, 'region', 'counts', 'house_type', address_out, 'Comm_by_regions_for_each_house_type',
                       caption, pdf, show_fig=show)
    print(c(caption, "yellow"), c('done', 'green'))
    # print()

    df_com = agg.commercials_for_category(df_full)
    # print(df_com)
    df_com = df_com.rename(columns={'com_type_col': 'commercials_by_type'})
    f.log_dataframe(df_com, 'Nuber of commercials by category', ['commercials_by_type', 'counts'], pdf, new_page=True)
    print(c("\t\tNuber of commercials by category: ", "yellow"), c('done', 'green'))
    # print()

    df_com = agg.commercials_for_house_type(df_full)
    # print(df_com)
    df_com = df_com.rename(columns={'house_type_col': 'houses_by_type'})
    f.log_dataframe(df_com, 'Nuber of commercials by house type', ['houses_by_type', 'counts'], pdf)
    print(c("\t\tNuber of commercials by house type: ", "yellow"), c('done', 'green'))

    # top max price sell
    columns_for_most = ['region', 'com_type', 'price_2']
    df_sell = agg.most_expensive(df_full, columns_for_most, 'sell').head(15)
    df_sell.insert(0, 'zone', df_sell.index)
    df_sell = df_sell.rename(columns={'zone': 'regions', 'price_2': 'cena(EUR)'})
    f.log_dataframe(df_sell, "Most Expensive Price in Each Region (first 15) - Sell : ", ['regions', 'cena(EUR)'], pdf,
                    new_page=True)
    print(c("\t\tMost Expensive Price in Each Region (first 15) - Sell : ", "yellow"), c('done', 'green'))

    # top max price rent
    df_sell = agg.most_expensive(df_full, columns_for_most, 'rent').head(15)
    df_sell.insert(0, 'zone', df_sell.index)
    df_sell = df_sell.rename(columns={'zone': 'regions', 'price_2': 'cena(EUR)'})
    f.log_dataframe(df_sell, "Most Expensive Price in Each Region (first 15) - Rent : ", ['regions', 'cena(EUR)'], pdf)
    print(c("\t\tMost Expensive Price in Each Region (first 15) - Rent : ", "yellow"), c('done', 'green'))

    # top avg price sell
    labels = {'zone': 'Regions', 'price_2': 'Cena (EUR)'}
    caption = "\t\tAverage Price in Each Region (first 10) - Sell : "
    df_sell = agg.average_price(df_full, columns_for_most, 'sell').head(10)
    df_sell.insert(0, 'zone', df_sell.index)
    f.plot_barchart(df_sell, 'zone', 'price_2', address_out, 'top_average_price_regions_sell', caption, pdf,
                    labels, show_fig=show)
    print(c(caption, "yellow"), c('done', 'green'))

    # top avg price rent
    caption = "\t\tAverage Price in Each Region (first 10) - Rent : "
    df_sell = agg.average_price(df_full, columns_for_most, 'rent').head(10)
    df_sell.insert(0, 'zone', df_sell.index)
    f.plot_barchart(df_sell, 'zone', 'price_2', address_out, 'top_average_price_regions_rent', caption, pdf,
                    labels, show_fig=show)
    print(c(caption, "yellow"), c('done', 'green'))

    # top avg price rent
    caption = "\t\tAverage Price in Each Region (first 10) - Rent(Day) : "
    df_sell = agg.average_price(df_full, columns_for_most, 'rent_by_day').head(10)
    df_sell.insert(0, 'zone', df_sell.index)
    f.plot_barchart(df_sell, 'zone', 'price_2', address_out, 'top_average_price_regions_rent_day', caption, pdf,
                    labels, show_fig=show)
    print(c(caption, "yellow"), c('done', 'green'))

    # geo
    columns_for_top_10 = ['region', 'street', 'rooms', 'floor', 'top_floor', 'm2', 'house_type', 'price_2']
    df_max = agg.max_top_n(df_full, columns_for_top_10, 'sell', 10)
    df_max = f.get_geo_data(df_max, use_proxy=use_proxy)
    # print(df_max.to_string(index=False))
    f.log_dataframe_with_geo_data(df_max, address_out, 'TOP 10 : SELL', 'top_10_sell_map', pdf, new_page=True)
    print(c("\t\tMost expensive commercial: (first 10) - Sell : ", "yellow"), c('done', 'green'))
    # print()

    df_max = agg.max_top_n(df_full, columns_for_top_10, 'rent', 10)
    df_max = f.get_geo_data(df_max, use_proxy=use_proxy)
    # print(df_max.to_string(index=False))
    f.log_dataframe_with_geo_data(df_max, address_out, 'TOP 10 : RENT', 'top_10_rent_map', pdf)
    print(c("\t\tMost expensive commercial: (first 10) - Rent : ", "yellow"), c('done', 'green'))
    # print()

    df_max = agg.max_top_n(df_full, columns_for_top_10, 'rent_by_day', 10)
    df_max = f.get_geo_data(df_max, use_proxy=use_proxy)
    # print(df_max.to_string(index=False))
    f.log_dataframe_with_geo_data(df_max, address_out, 'TOP 10 : RENT (DAY)', 'top_10_rent_day_map', pdf, new_page=True)
    print(c("\t\tMost expensive commercial: (first 10) - Rent(Day) : ", "yellow"), c('done', 'green'))
    # print()
    pdf.output(address_out/'data.pdf')

    # print(df_full.query(f"com_type == 'sell'").corr(method='pearson'))
    # print(df_full.query(f"com_type == 'rent'").corr(method='pearson'))
    # print(df_full.query(f"com_type == 'rent_by_day'").corr(method='pearson'))
    # print(df_full.dtypes)
