from utilz.PageAttributes import get_city, get_region, get_street, get_rooms, get_area_m2, get_floor, get_house_type, \
    get_price, get_date, get_location, get_house_rooms, get_outer_area_m2, get_floor_count, get_amenities

flats, houses = ('flats', 'houses')


def get_links_for_flats():
    return {'All': '',
            'Riga': 'https://www.ss.lv/lv/real-estate/flats/riga/all/',
            'Jurmala': 'https://www.ss.lv/lv/real-estate/flats/jurmala/all/',
            'Riga-reg': 'https://www.ss.lv/lv/real-estate/flats/riga-region/all/',
            'Aizkraukle-reg': 'https://www.ss.lv/lv/real-estate/flats/aizkraukle-and-reg/all/',
            'Aluksne-reg': 'https://www.ss.lv/lv/real-estate/flats/aluksne-and-reg/all/',
            'Balvi-reg': 'https://www.ss.lv/lv/real-estate/flats/balvi-and-reg/all/',
            'Bauska-reg': 'https://www.ss.lv/lv/real-estate/flats/bauska-and-reg/all/',
            'Cesis-reg': 'https://www.ss.lv/lv/real-estate/flats/cesis-and-reg/all/',
            'Daugavpils-reg': 'https://www.ss.lv/lv/real-estate/flats/daugavpils-and-reg/all/',
            'Dobele-reg': 'https://www.ss.lv/lv/real-estate/flats/dobele-and-reg/all/',
            'Gulbene-reg': 'https://www.ss.lv/lv/real-estate/flats/gulbene-and-reg/all/',
            'Jekabpils-reg': 'https://www.ss.lv/lv/real-estate/flats/jekabpils-and-reg/all/',
            'Jelgava-reg': 'https://www.ss.lv/lv/real-estate/flats/jelgava-and-reg/all/',
            'Kraslava-reg': 'https://www.ss.lv/lv/real-estate/flats/kraslava-and-reg/all/',
            'Kuldiga-reg': 'https://www.ss.lv/lv/real-estate/flats/kuldiga-and-reg/all/',
            'Liepaja-reg': 'https://www.ss.lv/lv/real-estate/flats/liepaja-and-reg/all/',
            'Limbadzi-reg': 'https://www.ss.lv/lv/real-estate/flats/limbadzi-and-reg/all/',
            'Ludza-reg': 'https://www.ss.lv/lv/real-estate/flats/ludza-and-reg/all/',
            'Madona-reg': 'https://www.ss.lv/lv/real-estate/flats/madona-and-reg/all/',
            'Ogre-reg': 'https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/all/'}


def get_links_for_houses():
    return {'All': '',
            'Riga': 'https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/all/',
            'Jurmala': 'https://www.ss.lv/lv/real-estate/homes-summer-residences/jurmala/all/',
            'Riga-reg': 'https://www.ss.lv/lv/real-estate/homes-summer-residences/riga-region/all/'}


def get_links(key):
    return linkz.get(key)


def enumerate_keys(dictionary):
    sequence = [x for x in range(len(dictionary.keys()))]
    return dict(zip(sequence, dictionary.keys()))


def print_dictionary(dictionary):
    [print(key, ' : ', val) for key, val in dictionary.items()]


elements_dispatcher = {
    flats: [get_city, get_region, get_street, get_rooms, get_area_m2, get_floor, get_house_type, get_price, get_date,
            get_location],
    houses: [get_city, get_region, get_street, get_house_rooms, get_outer_area_m2, get_area_m2, get_floor_count,
             get_amenities, get_price, get_date, get_location]}

linkz = {flats: get_links_for_flats(), houses: get_links_for_houses()}
columnz = {
    flats: ['description', 'link', 'city', 'region', 'street', 'rooms', 'm2', 'floor', 'house_type', 'price', 'date',
            'lat', 'long'],
    houses: ['description', 'link', 'city', 'region', 'street', 'rooms', 'out_m2', 'm2', 'floor', 'amenity', 'price',
             'date', 'lat', 'long']}
