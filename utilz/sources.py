def get_links_for_flats():
    return {'All': '',
            'Riga': 'https://www.ss.lv/lv/real-estate/flats/riga/all/',
            'Jurmala': 'https://www.ss.lv/lv/real-estate/flats/jurmala/all/',
            'Riga-Region': 'https://www.ss.lv/lv/real-estate/flats/riga-region/all/'}


def enumerate_keys(dictionary):
    sequence = [x for x in range(len(dictionary.keys()))]
    return dict(zip(sequence, dictionary.keys()))


def print_dictionary(dictionary):
    [print(key, ' : ', val) for key, val in dictionary.items()]

