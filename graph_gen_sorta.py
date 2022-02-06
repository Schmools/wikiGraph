# Samuel Schuur, 2021 (this worked at one point)

from os import read
from pathlib import Path
import json

from graph_tool.all import *

g = Graph(directed=False)

#read json file
filename = str(Path.cwd()) + "/graph.json"
print(filename)
with open(filename) as f:
    in_graph = json.load(f)

article_titles = in_graph["nodes"]

# accessing titles for stupid ppl like me
# print(article_titles[0]["id"])

g.add_vertex(len(article_titles))

title = g.new_vertex_property("string")

# this could also probably go in the linking loop
for v in g.vertices():
    title[v] = article_titles[int(v)]["id"]

article_links = in_graph["links"]

i = 0
article = article_links[0]["source"]

article_titles = [title["id"] for title in article_titles]

for dict in article_links:
    if(article != dict["source"]):
        i = i + 1

    g.add_edge(g.vertex(i), g.vertex(article_titles.index(dict["target"])))
    print(article + " --> " + dict["target"])

    article = dict["source"]

#filter stuff

tree = random_spanning_tree(g)
filter = g.new_vertex_property("bool")
for v in g.vertices():
    if title[v] == "Wayback Machine":
        filter[v] = 0
    else:
        filter[v] = 1

fg = GraphView(g, efilt=tree)
pos = graph_tool.draw.sfdp_layout(fg)

#interactive seems to fail past 1000
graph_draw(fg, output="nodes.svg", ink_scale = 0.5, pos=pos, vertex_text=title, vertex_text_position=0.1, output_size=(540,960))
