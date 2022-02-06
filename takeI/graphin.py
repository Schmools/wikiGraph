from os import read
from networkx.readwrite import json_graph
import json

from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx

import networkx

def read_json_file(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)

g = read_json_file(r"C:\Users\schuu\Documents\Git\wikiGraph\\graph.json")

#Choose a title!
title = "Wikipedia"

#Establish which categories will appear when hovering over each node
HOVER_TOOLTIPS = [("Character", "@index")]

#Create a plot — set dimensions, toolbar, and title
plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-2.55, 2.55), y_range=Range1d(-1.31, 1.31), title=title, plot_width=2550,  plot_height=1310)

#Create a network graph object with spring layout
# https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
network_graph = from_networkx(g, networkx.spring_layout, scale=10, center=(0, 0))

#Set node size and color
network_graph.node_renderer.glyph = Circle(size=10, fill_color='#CC7929')

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.1, line_width=1)

#Add network graph to the plot
plot.renderers.append(network_graph)

show(plot)