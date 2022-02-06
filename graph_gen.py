# Samuel Schuur, 2021

from os import read
from pathlib import Path
import json

from graph_tool.all import *

g = Graph(directed=False)

#read json file
filename = str(Path.cwd()) + "/graph2.json"
print(filename)
with open(filename) as f:
    in_graph = json.load(f)

article_titles = in_graph["nodes"]
article_titles = [title["id"] for title in article_titles]
article_links = in_graph["links"]

g.add_vertex(len(article_titles))
title = g.new_vertex_property("string")

# name the vertices
for vertex in g.vertices():
    title[vertex] = article_titles[int(vertex)]
    print(str(int(vertex)) + ":" + article_titles[int(vertex)])

# link vertices
for dict in article_links:
    source = article_titles.index(dict["source"])
    target = article_titles.index(dict["target"])
    g.add_edge(g.vertex(source), g.vertex(target))

    print(title[g.vertex(source)] + " --> " + title[g.vertex(target)])

g.remove_vertex(article_titles.index("Wayback Machine"))

tree = min_spanning_tree(g)
fg = GraphView(g, efilt=tree)

# drawing using graph-tools
# pos = sfdp_layout(fg, K=50, C=50)
# graph_draw(fg, pos=pos, output="nodes.pdf", ink_scale = 0.5, vertex_text=title, vertex_text_position=0.1, output_size=(1000,1000))

# draw using graphviz
vprops = {"xlabel":title}

graphviz_draw(fg, layout="sfdp", output="nodes.svg", overlap="scalexy", sep=2, vprops=vprops, ratio="auto", splines="True")
