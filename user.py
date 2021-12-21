"""User class and the operations on user objects."""
from __future__ import annotations

from typing import List, Tuple
import python_ta
import weighted_graph
import anime
import visualization

AnimeDict, AnimeSet = anime.main()
UserGraph, AnimeGraph = weighted_graph.main()


class User:
    """Someone who has an anime account

    Instance Attributes:
        - self.name: Users name
        - self.anime: All shows this user watches
        - self.weighted_anime: All shows this user watches, and their corresponding weight
        - self.genres: The genres the anime include
        - self.weighted_genres: The genres the anime include, and the prevalence of that genre
        - self.genre_sum: sum of weights of genres in weighted_genres
        - self.recommended: list of current recommended anime
        - self.weighted_recommended: list of current recommended anime
    """

    name: str
    anime: list[str]
    weighted_anime: list[tuple(str, int)]
    genres: list[str]
    weighted_genres: dict
    genre_sum: int
    recommended: list[str]
    weighted_recommended: list[tuple(str, int)]
    genre_weight: float

    def __init__(self, name: str, weighted_anime: list[tuple[str, int]]) -> None:
        """Initialize a new User
        """
        self.name = name
        self.weighted_anime = [x for x in weighted_anime if x[0] in AnimeSet]
        self.anime = [x[0] for x in self.weighted_anime]
        self.genre_weight = 0
        self.recommended = []
        self.weighted_recommended = []

        genres_set = set()
        for show in self.anime:
            genres_set.update(AnimeDict[show].genres)
        self.genres = list(genres_set)

        self.weighted_genres = dict()
        for show in self.weighted_anime:
            for genre in AnimeDict[show[0]].genres:
                if genre not in self.weighted_genres.keys():
                    self.weighted_genres[genre] = show[1]
                else:
                    self.weighted_genres[genre] += show[1]
                self.genre_weight += show[1]

    def genre_matches(self, anime_list: list[tuple[str, int]], genres: list[str])\
            -> List[Tuple[str, int]]:
        """Returns list of animes ranked by genre_similarity"""
        genre_total = []
        for show in anime_list:
            genre_total.append((show, self.genre_similarity(show[0], genres)))
        genre_total.sort(key=lambda x: x[1], reverse=True)
        animes = [x[0] for x in genre_total]
        return animes

    def genre_similarity(self, anime1: str, genres: list[str]) -> float:
        """returns similarity of anime to users genre taste,
        or the genre they decided to look for"""
        if genres == []:
            return sum([self.weighted_genres[x] for x in self.weighted_genres
                        if x in AnimeDict[anime1].genres]) / self.genre_weight

        return len([x for x in genres if x in AnimeDict[anime1].genres]) / len(genres)

    def recommend_shows(self, limit: int, alg_type: str, length: str,
                        genres: list[str], genre_check: bool) -> list[tuple[any, any, any, int]]:
        """Recommend shows to user based on their previously watched shows,
        and can account for specified show length, episode length, and genre"""
        if alg_type == 'User Comparison':
            graph = UserGraph
        else:
            graph = AnimeGraph
        unfiltered = graph.recommend(self.weighted_anime, 100, alg_type)
        if length is not None:
            unfiltered = [x for x in unfiltered if AnimeDict[x[0]].length == length]
        if genre_check or genres != []:
            unfiltered = self.genre_matches(unfiltered, genres)

        unfiltered.sort(key=lambda x: x[1], reverse=True)
        if len(unfiltered) > limit:
            unfiltered = unfiltered[:limit]

        self.weighted_recommended = unfiltered
        self.recommended = [x[0] for x in unfiltered]

        filtered = [(AnimeDict[x[0]].name, AnimeDict[x[0]].img, AnimeDict[x[0]].synopsis, x[1])
                    for x in unfiltered]
        return filtered

    def compare_user(self, other: User) -> float:
        """finds similarity of two users. Adds them to the graph
         and calculates their broad similarity score. Then removes them"""

        self.add_user_to_graph()

        other.add_user_to_graph()
        result = UserGraph.get_similarity_score(self.name, other.name, 'broad')

        UserGraph.remove_vertex(other.name)
        UserGraph.remove_vertex(self.name)

        return int(result * 100)

    def add_user_to_graph(self) -> None:
        """Adds given user, to UserGraph"""
        UserGraph.add_vertex(self.name, 'user')
        for show in self.weighted_anime:
            UserGraph.add_edge(self.name, show[0], show[1])

    def call_visualizer1(self) -> None:
        """calls the first graph visualization"""
        visualization.visualize_graph(AnimeGraph,
                                      weighted_recommended_anime=self.weighted_recommended,
                                      weighted_chosen_anime=self.weighted_anime)

    def call_visualizer2(self) -> None:
        """calls the second graph visualization"""
        paths_dict = AnimeGraph.find_paths(self.recommended[0], self.anime)
        special_graph = weighted_graph.make_special_graph(paths_dict)
        visualization.visualize_graph_special(special_graph, [self.weighted_recommended[0]],
                                              self.weighted_anime)

    def call_visualizer3(self) -> None:
        """calls the third graph visualization"""
        sorted_anime_weighting = sorted(self.weighted_anime, key=lambda score: score[1],
                                        reverse=True)
        paths_dict = AnimeGraph.find_paths(sorted_anime_weighting[0][0], self.recommended)
        special_graph = weighted_graph.make_special_graph(paths_dict)
        visualization.visualize_graph_special(special_graph, self.weighted_recommended,
                                              [sorted_anime_weighting[0]])


# python_ta.check_all(config={
#     'extra-imports': [],  # the names (strs) of imported modules
#     'allowed-io': [],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['E1136']
# })
