"""CSC111 Winter 2021 Project: Anime Atlas

Module Description
==================

This module contains some Python functions that we are using to visualize the graph that is going to
be displayed.
"""
import networkx as nx
import python_ta

import anime
from typing import Optional

from bokeh.io import show
from bokeh.models import Range1d, Circle, MultiLine, NodesAndLinkedEdges
from bokeh.plotting import figure, from_networkx, ColumnDataSource
from bokeh.palettes import Reds8, Greys8, Greens8, Spectral4
import weighted_graph

AnimeDict, AnimeSet = anime.main()


def to_networkx(graph: weighted_graph.WeightedGraph, chosen_anime: Optional[list],
                recommended_anime: Optional[list], max_vertices: int = 5000) -> nx.Graph:
    """Convert this graph into a networkx Graph.
    Optional arguments:
        - recommended_anime: a list containing the the ids of anime's which the user is being
            recommended
        - chosen_anime: a list containing the ids of anime's which the user chose.
        - max_vertices: the maximum number of vertices that can appear in the graph

    max_vertices specifies the maximum number of vertices that can appear in the graph.
    (This is necessary to limit the visualization output for large graphs.)

    """
    graph_nx = nx.Graph()
    for v in graph.vertices.values():
        if v.item in chosen_anime:
            graph_nx.add_node(AnimeDict[v.item].name,
                              kind=v.kind,
                              image=AnimeDict[v.item].img,
                              user_type="Chosen Anime",
                              color_code="#696")
        elif v.item in recommended_anime:
            graph_nx.add_node(AnimeDict[v.item].name,
                              kind=v.kind,
                              image=AnimeDict[v.item].img,
                              user_type="Recommended Anime",
                              color_code="#F00")
        else:
            graph_nx.add_node(AnimeDict[v.item].name,
                              kind=v.kind,
                              image=AnimeDict[v.item].img,
                              user_type="Other Anime",
                              color_code="#000")

        for u in v.neighbours:
            if graph_nx.number_of_nodes() < max_vertices:
                if u.item in chosen_anime:
                    graph_nx.add_node(AnimeDict[u.item].name,
                                      kind=u.kind,
                                      image=AnimeDict[u.item].img,
                                      user_type="Chosen Anime",
                                      color_code="#696")
                elif u.item in recommended_anime:
                    graph_nx.add_node(AnimeDict[u.item].name,
                                      kind=u.kind,
                                      image=AnimeDict[u.item].img,
                                      user_type="Recommended Anime",
                                      color_code="#F00")
                else:
                    graph_nx.add_node(AnimeDict[u.item].name,
                                      kind=u.kind,
                                      image=AnimeDict[u.item].img,
                                      user_type="Other Anime",
                                      color_code="#000")

            if AnimeDict[u.item].name in graph_nx.nodes:
                graph_nx.add_edge(AnimeDict[v.item].name, AnimeDict[u.item].name)
                graph_nx[AnimeDict[v.item].name][AnimeDict[u.item].name]['weight'] \
                    = u.neighbours[v]

        if graph_nx.number_of_nodes() >= max_vertices:
            break

    return graph_nx


def visualize_graph(graph: weighted_graph.WeightedGraph,
                    weighted_recommended_anime: Optional[list],
                    weighted_chosen_anime: Optional[list],
                    max_vertices: int = 5000) -> None:
    """Use bokeh.io and networkx to visualize the given graph.

    Optional arguments:
        - recommended_anime: a list containing the the ids of anime's which the user is being
            recommended
        - chosen_anime: a list containing the ids of anime's which the user chose.
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)

    max_vertices specifies the maximum number of vertices that can appear in the graph.
    (This is necessary to limit the visualization output for large graphs.)
    """
    recommended_anime = [x[0] for x in weighted_recommended_anime]
    chosen_anime = [x[0] for x in weighted_chosen_anime]
    # Converts WeightedAnimeGraph to networkx graph
    graph_nx = to_networkx(graph,
                           chosen_anime=chosen_anime,
                           recommended_anime=recommended_anime,
                           max_vertices=max_vertices)

    node_to_weighting = {}
    for x in weighted_recommended_anime:
        node_to_weighting[AnimeDict[x[0]].name] = x[1] * 2
        graph_nx.nodes[AnimeDict[x[0]].name]['weight'] = x[1]
    for x in weighted_chosen_anime:
        node_to_weighting[AnimeDict[x[0]].name] = x[1] * 2
        graph_nx.nodes[AnimeDict[x[0]].name]['weight'] = x[1]
    for node in graph_nx.nodes:
        if node not in node_to_weighting:
            node_to_weighting[node] = 5.0
            graph_nx.nodes[node]['weight'] = 0.0

    user_type = {}
    for u in graph_nx.nodes:
        user_type[u] = graph_nx.nodes[u]['user_type']
    user_type_list = list(user_type.values())

    # Calculates the kind of each node and stores the information in a dictionary with the format
    # {node: kind}
    kind = {}
    for u in graph_nx.nodes:
        kind[u] = graph_nx.nodes[u]['kind']

    # Setting node size attribute based on the number of neighbours a node has i.e. the more
    # neighbours a node has, the larger it will be.
    nx.set_node_attributes(graph_nx,
                           name='weighting',
                           values=node_to_weighting)

    user_node_color = {}
    for u in graph_nx.nodes:
        if graph_nx.nodes[u]["user_type"] == "Chosen Anime":
            user_node_color[u] = Greens8[2]
        elif graph_nx.nodes[u]["user_type"] == "Recommended Anime":
            user_node_color[u] = Reds8[2]
        else:
            user_node_color[u] = Greys8[0]
    node_color_list = list(user_node_color.values())

    nx.set_node_attributes(graph_nx,
                           name='colored_node',
                           values=user_node_color)

    # These categories will be displayed when the mouse is hovered over a node. We used a bit of
    # HTML to make the hover function more visually pleasing. Furthermore, it is only possible to
    # display images through this method. We are displaying the name (@index), the image (@image),
    # the kind (@kind) and the number of neighbours (@degree).
    HOVER_TOOLTIPS = """
                    <div>
                        <div>
                            <img
                                src="@image" height="120" alt="@image" width="85"
                                style="float: left; margin: 0px 15px 15px 0px;"
                                border="2"
                            ></img>
                        </div>
                            <span style="font-size: 17px; font-weight: bold;">@index</span>
                        <div>
                            <span style="font-size: 15px;">Kind: @kind</span>
                        <div>
                            <span style="font-size: 13.5px; color: @color_code;"> @user_type</span>
                        <div>
                            <span style="font-size: 12px;">Weighting: @weight</span>
                        </div>
                    </div>
                    """

    # Here we create a plot in which we set the dimensions, tooltips, tools, scrolling, the size of
    # the visualization, and we stretch the plot to fit any users display (universally).
    plot = figure(title='Anime Visualization',
                  tooltips=HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset",
                  active_scroll='wheel_zoom',
                  x_range=Range1d(-12.0, 12.0),
                  y_range=Range1d(-10.0, 10.0),
                  sizing_mode='stretch_both')

    position_dict = dict(nx.spring_layout(graph_nx)).values()
    positions = []
    x_pos = []
    y_pos = []
    for x in position_dict:
        positions.append(x)
    for x in positions:
        x_pos.append(x[0])
        y_pos.append(x[1])

    source = ColumnDataSource(dict(anime_names=list(graph_nx.nodes),
                                   x=x_pos,
                                   y=y_pos,
                                   color=node_color_list,
                                   label=user_type_list))

    plot.circle(x='x', y='y', radius=0.0, color='color', legend_group='label', source=source)

    # Here we are creating a network graph
    output_graph = from_networkx(graph_nx, nx.spring_layout,
                                 scale=10,
                                 center=(0, 0))

    output_graph.node_renderer.glyph = Circle(size='weighting',
                                              fill_color='colored_node')
    output_graph.node_renderer.selection_glyph = Circle(size='weighting',
                                                        fill_color=Spectral4[2])
    output_graph.node_renderer.hover_glyph = Circle(size='weighting',
                                                    fill_color=Spectral4[1])
    # Setting edge thickness based on the weight of 2 vertices.
    output_graph.edge_renderer.data_source.data["line_width"] = \
        [graph_nx.get_edge_data(u, v)['weight'] / 1.5 for u, v in graph_nx.edges()]

    output_graph.edge_renderer.glyph = MultiLine(line_color=Greys8[0])
    output_graph.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=2)
    output_graph.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=2)

    # Rendering line width
    output_graph.edge_renderer.glyph.line_width = {'field': 'line_width'}

    output_graph.selection_policy = NodesAndLinkedEdges()
    output_graph.inspection_policy = NodesAndLinkedEdges()

    # Rendering the entire graph
    plot.renderers.append(output_graph)

    # Shows the plot
    show(plot)


def visualize_graph_special(graph: weighted_graph.WeightedGraph,
                    weighted_recommended_anime: Optional[list],
                    weighted_chosen_anime: Optional[list],
                    max_vertices: int = 5000) -> None:
    """Use bokeh.io and networkx to visualize the given graph. Note that the graph inputted was
    created using a special algorithm.

    Optional arguments:
        - recommended_anime: a list containing the the ids of anime's which the user is being
            recommended
        - chosen_anime: a list containing the ids of anime's which the user chose.
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)

    max_vertices specifies the maximum number of vertices that can appear in the graph.
    (This is necessary to limit the visualization output for large graphs.)
    """
    recommended_anime = [x[0] for x in weighted_recommended_anime]
    chosen_anime = [x[0] for x in weighted_chosen_anime]
    combined_list = weighted_recommended_anime + weighted_chosen_anime
    # Converts WeightedAnimeGraph to networkx graph
    graph_nx = to_networkx(graph,
                           chosen_anime=chosen_anime,
                           recommended_anime=recommended_anime,
                           max_vertices=max_vertices)

    id_to_weight = dict(combined_list)
    print(id_to_weight)
    node_to_weighting = {}
    for key in id_to_weight.keys():
        if key in AnimeDict:
            node_to_weighting[AnimeDict[key].name] = id_to_weight[key] + 5
    for node in graph_nx.nodes:
        if node in node_to_weighting:
            graph_nx.nodes[node]['weight'] = node_to_weighting[node]
        else:
            node_to_weighting[node] = 5.0
            graph_nx.nodes[node]['weight'] = 0.0

    user_type = {}
    for u in graph_nx.nodes:
        user_type[u] = graph_nx.nodes[u]['user_type']
    user_type_list = list(user_type.values())

    # Calculates the kind of each node and stores the information in a dictionary with the format
    # {node: kind}
    kind = {}
    for u in graph_nx.nodes:
        kind[u] = graph_nx.nodes[u]['kind']

    # Setting node size attribute based on the number of neighbours a node has i.e. the more
    # neighbours a node has, the larger it will be.
    nx.set_node_attributes(graph_nx,
                           name='weighting',
                           values=node_to_weighting)

    user_node_color = {}
    for u in graph_nx.nodes:
        if graph_nx.nodes[u]["user_type"] == "Chosen Anime":
            user_node_color[u] = Greens8[2]
        elif graph_nx.nodes[u]["user_type"] == "Recommended Anime":
            user_node_color[u] = Reds8[2]
        else:
            user_node_color[u] = Greys8[0]
    node_color_list = list(user_node_color.values())

    nx.set_node_attributes(graph_nx,
                           name='colored_node',
                           values=user_node_color)

    # These categories will be displayed when the mouse is hovered over a node. We used a bit of
    # HTML to make the hover function more visually pleasing. Furthermore, it is only possible to
    # display images through this method. We are displaying the name (@index), the image (@image),
    # the kind (@kind) and the number of neighbours (@degree).
    HOVER_TOOLTIPS = """
                    <div>
                        <div>
                            <img
                                src="@image" height="120" alt="@image" width="85"
                                style="float: left; margin: 0px 15px 15px 0px;"
                                border="2"
                            ></img>
                        </div>
                            <span style="font-size: 17px; font-weight: bold;">@index</span>
                        <div>
                            <span style="font-size: 15px;">Kind: @kind</span>
                        <div>
                            <span style="font-size: 13.5px; color: @color_code;"> @user_type</span>
                        <div>
                            <span style="font-size: 12px;">Weighting: @weight</span>
                        </div>
                    </div>
                    """

    # Here we create a plot in which we set the dimensions, tooltips, tools, scrolling, the size of
    # the visualization, and we stretch the plot to fit any users display (universally).
    plot = figure(title='Anime Visualization',
                  tooltips=HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset",
                  active_scroll='wheel_zoom',
                  x_range=Range1d(-12.0, 12.0),
                  y_range=Range1d(-10.0, 10.0),
                  sizing_mode='stretch_both')

    position_dict = dict(nx.spring_layout(graph_nx)).values()
    positions = []
    x_pos = []
    y_pos = []
    for x in position_dict:
        positions.append(x)
    for x in positions:
        x_pos.append(x[0])
        y_pos.append(x[1])

    source = ColumnDataSource(dict(anime_names=list(graph_nx.nodes),
                                   x=x_pos,
                                   y=y_pos,
                                   color=node_color_list,
                                   label=user_type_list))

    plot.circle(x='x', y='y', radius=0.0, color='color', legend_group='label', source=source)

    # Here we are creating a network graph
    output_graph = from_networkx(graph_nx, nx.spring_layout,
                                 scale=10,
                                 center=(0, 0))

    output_graph.node_renderer.glyph = Circle(size='weighting',
                                              fill_color='colored_node')
    output_graph.node_renderer.selection_glyph = Circle(size='weighting',
                                                        fill_color=Spectral4[2])
    output_graph.node_renderer.hover_glyph = Circle(size='weighting',
                                                    fill_color=Spectral4[1])
    # Setting edge thickness based on the weight of 2 vertices.
    output_graph.edge_renderer.data_source.data["line_width"] = \
        [graph_nx.get_edge_data(u, v)['weight'] / 1.5 for u, v in graph_nx.edges()]

    output_graph.edge_renderer.glyph = MultiLine(line_color=Greys8[0])
    output_graph.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=2)
    output_graph.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=2)

    # Rendering line width
    output_graph.edge_renderer.glyph.line_width = {'field': 'line_width'}

    output_graph.selection_policy = NodesAndLinkedEdges()
    output_graph.inspection_policy = NodesAndLinkedEdges()

    # Rendering the entire graph
    plot.renderers.append(output_graph)

    # Shows the plot
    show(plot)


# python_ta.check_all(config={
#     'extra-imports': [],  # the names (strs) of imported modules
#     'allowed-io': [],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['E1136']
# })
