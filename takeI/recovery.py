# Samuel Schuur, 2021
# trying to recover this half broken code, lol

import wikipedia

import os

import networkx as nx
import json
from networkx.readwrite import json_graph

filename = r"C:\Users\schuu\Documents\Git\wikiGraph\\articleList.txt"

with open(filename, encoding="utf-8") as f:
    list = f.read().split("\n")



g = nx.Graph()

wikiList = []

for entry in list:
    if("https://" in entry):
        continue

    g.add_node(entry)
    wikiList.append(entry)

print("wikilist done!") 
#print(wikiList)

def pageSearch(entry):
   try:
       search = wikipedia.search(entry)
       return wikipedia.page(search[0], auto_suggest=False)
   except wikipedia.exceptions.DisambiguationError as e:
       print(e)

for entry in wikiList:
    try:
        print(entry) 
        page = pageSearch(entry)
        for link in page.links:
            #print(link)
            if(link in wikiList):
                print(entry + " --> " + link)
                g.add_edge(entry, link)
    except:
        print("error")

data = json_graph.node_link_data(g)
with open('graph.json', 'w') as f:
    json.dump(data, f, indent=4)