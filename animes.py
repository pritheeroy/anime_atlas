"""
Generates the anime we look at in our recommendation system.
"""
import python_ta
import json
import webscrapping


action = []
adventure = []
comedy = []
drama = []
sci_fi = []
slice_of_life = []
seinen = []
fantasy = []
mystery = []
psych = []
romance = []
sports = []
mecha = []
ecchi = []
horror = []


def top_action() -> None:
    """Aggregates a list of the most famous action anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/8/Drama", action)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/8/Drama?page=2", action)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/8/Drama?page=3", action)


def top_adventure() -> None:
    """Aggregates a list of the most famous adventure anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/2/Adventure", adventure)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/2/Adventure?page=2", adventure)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/2/Adventure?page=3", adventure)


def top_comedy() -> None:
    """Aggregates a list of the most famous comedy anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/4/Comedy", comedy)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/4/Comedy?page=2", comedy)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/4/Comedy?page=3", comedy)


def top_drama() -> None:
    """Aggregates a list of the most famous drama anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/8/Drama", drama)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/8/Drama?page=2", drama)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/8/Drama?page=3", drama)


def top_sci_fi() -> None:
    """Aggregates a list of the most famous sci-fi anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/24/Sci-Fi", sci_fi)

    def recursive_append(lst: list, url: str) -> None:
        """Aggregated a list without duplicate shows recursively"""
        temp = []
        webscrapping.genre_scrap(url, temp)
        for show in temp:
            if show not in lst:
                lst.append(show)

    recursive_append(sci_fi, "https://myanimelist.net/anime/genre/37/Supernatural")
    recursive_append(sci_fi, "https://myanimelist.net/anime/genre/24/Sci-Fi?page=2")
    recursive_append(sci_fi, "https://myanimelist.net/anime/genre/37/Supernatural?page=2")


def top_slice_of_life() -> None:
    """Aggregates a list of the most famous slice of life anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/36/Slice_of_Life", slice_of_life)

    def recursive_append(lst: list, url: str) -> None:
        """Aggregated a list without duplicate shows recursively"""
        temp = []
        webscrapping.genre_scrap(url, temp)
        for show in temp:
            if show not in lst:
                lst.append(show)

    recursive_append(slice_of_life, "https://myanimelist.net/anime/genre/23/School")
    recursive_append(slice_of_life, "https://myanimelist.net/anime/genre/36/Slice_of_Life?page=2")
    recursive_append(slice_of_life, "https://myanimelist.net/anime/genre/23/School?page=2")


def top_seinen() -> None:
    """Aggregates a list of the most famous seinen anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/42/Seinen", seinen)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/42/Seinen?page=2", seinen)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/42/Seinen?page=3", seinen)


def top_fantasy() -> None:
    """Aggregates a list of the most famous fantasy anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/10/Fantasy", fantasy)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/10/Fantasy?page=2", fantasy)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/10/Fantasy?page=3", fantasy)


def top_mystery() -> None:
    """Aggregates a list of the most famous mystery anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/7/Mystery", mystery)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/7/Mystery?page=2", mystery)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/7/Mystery?page=3", mystery)


def top_psych() -> None:
    """Aggregates a list of the most famous psychological anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/40/Psychological", psych)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/40/Psychological?page=2", psych)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/40/Psychological?page=3", psych)


def top_romance() -> None:
    """Aggregates a list of the most famous romance anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/22/Romance", romance)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/22/Romance?page=2", romance)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/22/Romance?page=3", romance)


def top_sports() -> None:
    """Aggregates a list of the most famous sports anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/30/Sports", sports)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/30/Sports?page=2", sports)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/30/Sports?page=3", sports)


def top_mecha() -> None:
    """Aggregates a list of the most famous mecha anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/18/Mecha", mecha)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/18/Mecha?page=2", mecha)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/18/Mecha?page=3", mecha)


def top_ecchi() -> None:
    """Aggregates a list of the most famous ecchi anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/9/Ecchi", ecchi)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/9/Ecchi?page=2", ecchi)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/9/Ecchi?page=3", ecchi)


def top_horror() -> None:
    """Aggregates a list of the most famous ecchi anime through web-scrapping"""
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/14/Horror", horror)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/14/Horror?page=2", horror)
    webscrapping.genre_scrap("https://myanimelist.net/anime/genre/14/Horror?page=3", horror)


def populate() -> None:
    """Populates anime genre lists"""
    top_action()
    top_adventure()
    top_comedy()
    top_drama()
    top_sci_fi()
    top_slice_of_life()
    top_seinen()
    top_fantasy()
    top_mystery()
    top_psych()
    top_romance()
    top_sports()
    top_mecha()
    top_ecchi()
    top_horror()


def top_500() -> None:
    """Aggregates a list of the most relevant 850 anime to the user

    Preconditions:
        - populate() has been ran successfully
        - len(genre) > 300, where genre is any list initialized
        - path to id_data.json is valid
    """
    five_hundo = [5114,
                  38524,
                  9253,
                  28977,
                  11061,
                  9969,
                  820,
                  40028,
                  15417,
                  35180,
                  28851,
                  34096,
                  4181,
                  918,
                  15335,
                  32281,
                  35247,
                  2904,
                  37491,
                  33050,
                  32935,
                  37510,
                  31758,
                  199,
                  36838,
                  39486,
                  40748,
                  17074,
                  33095,
                  1,
                  19,
                  41025,
                  24701,
                  263,
                  42938,
                  34599,
                  36862,
                  40456,
                  21939,
                  44,
                  23273,
                  37987,
                  37521,
                  1575,
                  28891,
                  40591,
                  164,
                  245,
                  457,
                  11665,
                  38329,
                  2001,
                  2921,
                  5258,
                  431,
                  7311,
                  34591,
                  33352,
                  12355,
                  22135,
                  42203,
                  37779,
                  1535,
                  28957,
                  35760,
                  31757,
                  37991,
                  38000,
                  28735,
                  7785,
                  10379,
                  33049,
                  11741,
                  19647,
                  36098,
                  32983,
                  4565,
                  38474,
                  12365,
                  21329,
                  44042,
                  4282,
                  35839,
                  5300,
                  30276,
                  40776,
                  40417,
                  801,
                  30654,
                  35843,
                  21,
                  44070,
                  32,
                  170,
                  12431,
                  3297,
                  7472,
                  44087,
                  578,
                  38040]

    s_tier = [action, adventure, comedy, drama]
    a_tier = [sci_fi, slice_of_life, seinen, fantasy]
    b_tier = [mystery, psych, romance, horror]
    c_tier = [sports, mecha, ecchi]

    for genre in c_tier:
        temp = []
        for show in genre:
            if show not in five_hundo:
                temp.append(show)
        five_hundo = five_hundo + temp[:50]

    for genre in b_tier:
        temp = []
        for show in genre:
            if show not in five_hundo:
                temp.append(show)
        five_hundo = five_hundo + temp[:50]

    for genre in a_tier:
        temp = []
        for show in genre:
            if show not in five_hundo:
                temp.append(show)
        five_hundo = five_hundo + temp[:50]

    for genre in s_tier:
        temp = []
        for show in genre:
            if show not in five_hundo:
                temp.append(show)
        five_hundo = five_hundo + temp[:50]

    with open('id_data.json', 'w') as fp:
        json.dump(five_hundo, fp, sort_keys=True, indent=1)


populate()
# python_ta.check_all(config={
#     'extra-imports': [],  # the names (strs) of imported modules
#     'allowed-io': [],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['E1136']
# })
