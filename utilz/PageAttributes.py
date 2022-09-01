def get_city(current_info, internal_page_content):
    city = internal_page_content.find("td", class_="ads_opt", id="tdo_20")
    current_info.append(getattr(city, 'text', ''))


def get_region(current_info, internal_page_content):
    region = internal_page_content.find("td", class_="ads_opt", id="tdo_856")
    current_info.append(getattr(region, 'text', ''))


def get_street(current_info, internal_page_content):
    street = internal_page_content.find("td", class_="ads_opt", id="tdo_11")
    current_info.append(street.text.replace(" [Karte]", "") if street is not None else '')


def get_rooms(current_info, internal_page_content):
    room = internal_page_content.find("td", class_="ads_opt", id="tdo_1")
    current_info.append(getattr(room, 'text', ''))


def get_house_rooms(current_info, internal_page_content):
    room = internal_page_content.find("td", class_="ads_opt", id="tdo_58")
    current_info.append(getattr(room, 'text', ''))


def get_area_m2(current_info, internal_page_content):
    m2 = internal_page_content.find("td", class_="ads_opt", id="tdo_3")
    current_info.append(m2.text.replace(" m²", "") if m2 is not None else '')


def get_outer_area_m2(current_info, internal_page_content):
    m2 = internal_page_content.find("td", class_="ads_opt", id="tdo_60")
    current_info.append(m2.text.replace(" m²", "") if m2 is not None else '')


def get_floor(current_info, internal_page_content):
    floor = internal_page_content.find("td", class_="ads_opt", id="tdo_4")
    current_info.append(floor.text.replace("/lifts", "") if floor is not None else '')


def get_floor_count(current_info, internal_page_content):
    floor = internal_page_content.find("td", class_="ads_opt", id="tdo_57")
    current_info.append(floor.text.replace("/lifts", "") if floor is not None else '')


def get_amenities(current_info, internal_page_content):
    amenity = internal_page_content.find("td", class_="ads_opt", id="tdo_59")
    current_info.append(getattr(amenity, 'text', ''))


def get_house_type(current_info, internal_page_content):
    house = internal_page_content.find("td", class_="ads_opt", id="tdo_6")
    current_info.append(getattr(house, 'text', ''))


def get_price(current_info, internal_page_content):
    price = internal_page_content.find("td", class_="ads_price", id="tdo_8")
    current_info.append(getattr(price, 'text', ''))


def get_date(current_info, internal_page_content):
    footer = internal_page_content.find_all("td", class_="msg_footer")
    try:
        date_raw = footer[2].string
    except IndexError as ie:
        date_raw = "Datums: 01.01.1970 00:00"
    current_info.append(date_raw)


def get_location(current_info, internal_page_content):
    coordinates_element = internal_page_content.find("a", class_="ads_opt_link_map")
    try:
        coord_arr = coordinates_element.attrs['onclick'].split("=1&c=")[1].split(",")
    except AttributeError as ae:
        coord_arr = [0.0, 0.0]
    current_info.append(coord_arr[0])
    current_info.append(coord_arr[1])


elements_dispatcher = {'flats': [get_city, get_region, get_street, get_rooms, get_area_m2, get_floor, get_house_type, get_price, get_date, get_location],
                       'houses': [get_city, get_region, get_street, get_house_rooms, get_outer_area_m2, get_area_m2, get_floor_count, get_amenities, get_price, get_date, get_location]}
