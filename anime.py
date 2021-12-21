"""Anime class and the operations on an anime object."""
import json

from typing import Dict, List, Set

import python_ta


class Anime:
    """One show

    Instance Attributes:
        - name: name of anime
        - img: photo of anime
        - length: Total episodes
        - runtime: Length per episode
        - genres: Genres this anime fits into
    """
    name: str
    img: str
    length: str
    synopsis: str
    genres: List[str]

    def __init__(self, name: str, img: str, length: str, synopsis: str,
                 genres: List[str] = list) -> None:
        """Initialize a new vertex with the given item.

        This vertex is initialized with no neighbours.

        """
        self.name = name
        self.img = img
        self.length = length
        self.synopsis = synopsis
        self.genres = genres


def load_anime_dict() -> Dict[str, Anime]:
    """Creates a dictionary of anime."""
    anime_dict = dict()
    with open('show_data.json', 'r+') as f:
        data = json.load(f)
    for shown in data:
        show = data[shown]
        anime_dict[shown] = Anime(show[0], show[1], show[2], show[3], show[4])

    return anime_dict


def main() -> (Dict[int, Anime], Set[int]):
    """Returns a tuple of the keys of anime_dict with anime_dict"""
    anime_dict = load_anime_dict()
    anime_set = {x for x in anime_dict}
    return (anime_dict, anime_set)


# python_ta.check_all(config={
#     'extra-imports': [],  # the names (strs) of imported modules
#     'allowed-io': [],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['E1136']
# })
