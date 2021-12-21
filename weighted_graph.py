"""Creating the weighted graph and the functions operating on it."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Union

import python_ta


class WeightedVertex:
    """A vertex in a weighted anime review graph, used to represent one anime.

    Instance Attributes:
        - item: The data stored in this vertex, representing an anime
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    kind: str
    neighbours: dict[WeightedVertex, Union[int, float]]

    def __init__(self, item: Any, kind: str = '') -> None:
        """Initialize a new vertex with the given item.

        This vertex is initialized with no neighbours.

        """
        self.item = item
        self.kind = kind
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def get_weight(self, other: WeightedVertex) -> Union[int, float]:
        """Returns weight of edge, or 0 if none"""
        if other in self.neighbours:
            return self.neighbours[other]
        return 0

    def average_weight(self) -> float:
        """finds total weighting of all neighbours"""
        return self.total_weight() / self.degree()

    def total_weight(self) -> float:
        """finds total weighting of all neighbours"""
        return sum([self.neighbours[x] for x in self.neighbours])

    def rank_neighbours(self) -> list[WeightedVertex]:
        """returns list of neighbours ranked by weighting to them"""
        lst = [(x, self.neighbours[x]) for x in self.neighbours]
        lst.sort(key=lambda x: x[1], reverse=True)
        new_lst = [x[0] for x in lst]
        return new_lst

    def similarity_score(self, other: WeightedVertex, type1: str = 'strict') -> float:
        """Finds total anime's in which both are neighbours of, and adds 3 minus the difference of
        their weightings  to that edge. Divides this values by total anime's either of the two
        are neighbours with.
        """
        top = 0
        for neighb in self.neighbours:
            if neighb in other.neighbours.keys():
                if type1 == 'broad':
                    difference = abs(self.neighbours[neighb] - other.neighbours[neighb])
                    top += (3 - difference)
                elif type1 == 'sum':
                    sum1 = self.neighbours[neighb] + other.neighbours[neighb]
                    top += sum1
                else:
                    if self.neighbours[neighb] == other.neighbours[neighb]:
                        top += 1
        bottom_set = set(self.neighbours).union(set(other.neighbours))
        bottom = len(bottom_set)
        if bottom == 0:
            return 0
        return top / bottom


class WeightedGraph:
    """A weighted graph used to represent an anime review network that keeps track of review scores.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    vertices: dict[Any, WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        """
        if item not in self.vertices:
            self.vertices[item] = WeightedVertex(item, kind)

    def remove_vertex(self, vert: Any) -> None:
        """remove given vertex from this graph.

        Do nothing if the given item isn't already in this graph.

        """
        if vert in self.vertices:
            for vertex in self.vertices[vert].neighbours:
                vertex.neighbours.pop(self.vertices[vert])

        self.vertices.pop(vert)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph."""
        if kind == '':
            return set(self.vertices.keys())
        else:
            return {v.item for v in self.vertices.values() if v.kind == kind}

    def get_similarity_score(self, item1: Any, item2: Any, type1: str = 'strict') -> float:
        """Return the similarity score between the two given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        """
        if item1 not in self.vertices or item2 not in self.vertices:
            raise ValueError

        return self.vertices[item1].similarity_score(self.vertices[item2], type1)

    def recommend(self, anime: list[tuple[str, int]], limit: int,
                  type1: str = '') -> list[tuple[str, float]]:
        """Chooses which recommendation algorithm to use, and sorts, limits, and returns
         the final selection after calling that algorithm"""
        if type1 == 'User Comparison':
            anime_scores = self.recommend_anime_user(anime)
        elif type1 == 'Weighting':
            anime_scores = self.recommend_anime_weights(anime)
        elif type1 == 'Similarity':
            anime_scores = self.recommend_anime_neighbours(anime)
        else:
            anime_scores = self.recommend_anime_path(anime)

        anime_scores.sort(key=lambda x: x[1], reverse=True)
        if len(anime_scores) > limit:
            anime_scores = anime_scores[:limit]
        return anime_scores

    def recommend_anime_weights(self, anime: list[tuple[str, int]]) -> list[tuple[str, float]]:
        """Recommends anime based on which have the highest sum of
         weights of edges with the given anime"""
        totals = dict()

        animes = [self.vertices[x[0]] for x in anime]

        for show in anime:
            for neighb in self.vertices[show[0]].neighbours:
                if neighb not in animes:
                    effect = self.vertices[show[0]].neighbours[neighb] * (show[1] - 5)
                    if neighb in totals.keys():
                        totals[neighb] += effect
                    else:
                        totals[neighb] = effect

        anime_scores = [(x.item, totals[x]) for x in totals.keys()]
        return anime_scores

    def recommend_anime_neighbours(self, anime: list[tuple[str, int]]) -> list[tuple[str, float]]:
        """Recommends anime based on the sum of their similarity to the given anime."""

        animes = [x[0] for x in anime]

        anime_scores = []

        for show in self.vertices:
            if show not in animes:
                shared_similarity = 0
                for show2 in anime:
                    shared_similarity += self.get_similarity_score(show, show2[0], 'sum') * \
                                         (show2[1] - 5)
                anime_scores.append((show, shared_similarity))

        # list of tuples of shows that are neighbours to one or more show in anime,
        # and their total broad similarity to all given anime

        return anime_scores

    def recommend_anime_path(self, anime: list[tuple[str, int]]) -> list[tuple[str, float]]:
        """Recommends anime based on which"""

        animes = [x[0] for x in anime]
        other_shows = [self.vertices[x] for x in self.vertices if x not in animes]
        other_shows_dict = {x: 0 for x in other_shows}

        for show in anime:
            vert = self.vertices[show[0]]
            comparisons = self.find_path_recursion(other_shows, [[vert]], [vert], dict())
            for show2 in comparisons:
                pathway = comparisons[show2]
                edge_score = 0
                for vert in range(0, len(pathway) - 1):
                    edge_score += pathway[vert].neighbours[pathway[vert + 1]]
                edge_score /= (len(pathway) - 1) * (len(pathway) - 1)
                other_shows_dict[show2] += (edge_score * (show[1] - 5))

        anime_scores = [(x.item, other_shows_dict[x]) for x in other_shows_dict]

        return anime_scores

    def recommend_anime_user(self, anime: list[tuple[str, int]]) -> list[tuple[str, float]]:
        """Recommends anime based on which users this user is most similar to, and chooses the anime
        those users like that this user hasn't yet seen. Unlike the other 3 algorithms, this one
        uses the user-anime graph, rather than just the pure anime graph."""

        self.add_vertex('me', '')
        for show in anime:
            self.add_edge('me', show[0], show[1])
        # adds user to UserGraph

        user_totals = []
        for user in self.get_all_vertices('user'):
            result = self.get_similarity_score('me', user, 'broad')
            user_totals.append((user, result))
        # finds similarity of this user to all other users in UserGraph

        user_totals.sort(key=lambda x: x[1], reverse=True)
        top_users = user_totals[:15]
        # Takes 15 users most similar to this user

        animes = [self.vertices[x[0]] for x in anime]  # list of only the anime names in anime
        anime_options = dict()

        for user in top_users:
            for show in self.vertices[user[0]].neighbours:
                if show not in animes:
                    addon = user[1] * (self.vertices[user[0]].neighbours[show] - 5)
                    if show not in anime_options:
                        anime_options[show] = [addon, 1.0]
                    else:
                        anime_options[show][0] += addon
                        anime_options[show][1] += 1
        # Looking at all shows the top 15 users are neighbours of, finds those
        # with the highest overall (weight * similarity of this user)

        anime_scores = [(x.item, anime_options[x][0] / anime_options[x][1]) for x in anime_options]
        # finds shows with highest average scoring by the users, excluding shows of which only
        # one top user reviewed. This is to allow this algorithm to recommend more
        # niche shows, by finding users with very similar tastes, and recommending shows they liked
        # even if they are less well known

        return anime_scores

    def find_paths(self, start: str, end: list[str]) -> dict[WeightedVertex, list[WeightedVertex]]:
        """Finds shortest paths between a given vertex and a list of vertices"""
        star_v = self.vertices[start]
        end_v = [self.vertices[x] for x in end]
        return self.find_path_recursion(end_v, [[star_v]], [star_v], dict())

    def find_path_recursion(self, find: list[WeightedVertex], to_search: list[list[WeightedVertex]],
                            searched: list[WeightedVertex],
                            roots: dict[WeightedVertex, list[WeightedVertex]]) \
            -> dict[WeightedVertex, list[WeightedVertex]]:
        """Helper function to find_path"""

        new_search = []

        for show in to_search:
            for neighb in show[len(show) - 1].neighbours:
                if neighb not in searched:
                    searched.append(neighb)
                    show_copy = show + [neighb]
                    if neighb in find:
                        roots[neighb] = show_copy
                    if len(roots) == len(find) - 1:
                        return roots
                    new_search.append(show_copy)

        return self.find_path_recursion(find, new_search, searched, roots)


def make_special_graph(all_roots: dict[WeightedVertex, list[WeightedVertex]]) -> WeightedGraph:
    """
    Returns graph rooting from main vertex and stemming to the roots.
    Key of all_roots dict is the root of a graph.
    """
    a = WeightedGraph()
    for key in all_roots.keys():
        for vertex in all_roots[key]:
            if vertex not in a.vertices:
                a.add_vertex(vertex.item, 'show')

    for key in all_roots.keys():
        for i in range(0, len(all_roots[key]) - 1):
            a.add_edge(all_roots[key][i].item, all_roots[key][i + 1].item,
                       all_roots[key][i].neighbours[all_roots[key][i + 1]])

    return a


def load_weighted_review_graph() -> WeightedGraph:
    """Return an anime review WEIGHTED graph corresponding to the given datasets.
    """
    a = WeightedGraph()
    with open('user_data.json5', 'r+') as f:
        data = json.load(f)

    for user in data:
        a.add_vertex(user, 'user')
        for show in data[user]:
            a.add_vertex(show[0], 'show')
            a.add_edge(user, show[0], show[1])

    return a


def create_anime_graph(review_graph: WeightedGraph,
                       threshold: float = 0.5) -> WeightedGraph:
    """Return an anime graph based on the given review_graph."""

    anime_graph = WeightedGraph()

    for vertex in review_graph.get_all_vertices('show'):
        anime_graph.add_vertex(vertex, 'show')

    abe = anime_graph.get_all_vertices('show')

    for vertex in abe:
        for vertex2 in abe:
            if vertex != vertex2:
                similarity = review_graph.get_similarity_score(vertex, vertex2, 'broad')
                if similarity > threshold:
                    anime_graph.add_edge(vertex, vertex2, similarity)

    return anime_graph


def create_anime_graph2(review_graph: WeightedGraph,
                        threshold: float = 0.5) -> WeightedGraph:
    """Return an anime graph based on the given review_graph."""

    anime_graph = WeightedGraph()

    for vertex in review_graph.get_all_vertices('show'):
        anime_graph.add_vertex(vertex, 'show')

    abe = list(anime_graph.get_all_vertices('show'))
    vertices = {x: [[], 0.0] for x in abe}

    for vert in range(0, len(abe)):
        vertex = abe[vert]
        for vert2 in range(vert + 1, len(abe)):
            vertex2 = abe[vert2]
            if vertex != vertex2:
                similarity = review_graph.get_similarity_score(vertex, vertex2, 'broad')
                vertices[vertex][0].append((vertex2, similarity))
                vertices[vertex][1] += similarity
                vertices[vertex2][0].append((vertex, similarity))
                vertices[vertex][1] += similarity

        vertices[vertex][0].sort(key=lambda x: x[1], reverse=True)

    vertices_list = [(x, vertices[x]) for x in vertices]
    vertices_list.sort(key=lambda x: x[1][1], reverse=True)

    for vertex in vertices_list:
        i = 0
        while anime_graph.vertices[vertex[0]].degree() < threshold:
            if anime_graph.vertices[vertex[1][0][i][0]].degree() < threshold:
                if vertex[1][0][i][1] > 0.1:
                    anime_graph.add_edge(vertex[0], vertex[1][0][i][0], vertex[1][0][i][1])
            if i == len(vertex[1][0]) - 1:
                break
            i += 1

    return anime_graph


def main() -> (WeightedGraph, WeightedGraph):
    """Main File"""
    review_graph = load_weighted_review_graph()
    anime_graph = create_anime_graph2(review_graph, 10)
    # numberlist = anime_graph.get_all_vertices('show')
    # with open('show_data.json', 'r+') as f:
    #     data2 = json.load(f)
    # new_data = dict()
    # for num in numberlist:
    #     new_data[num] = data2[num]
    # f.close()
    # with open('show_data2.json5', 'w') as f:
    #     json.dump(new_data, f, sort_keys=True, indent=1)
    return (review_graph, anime_graph)


# python_ta.check_all(config={
#     'extra-imports': [],  # the names (strs) of imported modules
#     'allowed-io': [],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['E1136']
# })
