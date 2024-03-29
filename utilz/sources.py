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


linkz = {flats: get_links_for_flats(), houses: get_links_for_houses()}
columnz = {
    flats: ['description', 'link', 'city', 'region', 'street', 'rooms', 'm2', 'floor', 'house_type', 'price', 'date',
            'lat', 'long'],
    houses: ['description', 'link', 'city', 'region', 'street', 'rooms', 'out_m2', 'm2', 'floor', 'amenity', 'price',
             'date', 'lat', 'long']}
