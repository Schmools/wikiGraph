import sqlite3
import os

from bs4 import BeautifulSoup
from networkx.classes import graph
import requests

import wikipedia

import networkx as nx
import json
from networkx.readwrite import json_graph

#timer stuff
import time


def graphFunc():

    path = os.path.expanduser('~') + "\AppData\Roaming\Mozilla\Firefox\Profiles\\bsdak20f.default-release"
    db = os.path.join(path, 'places.sqlite')

    #print(db)

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    select_statement = "select moz_places.url, moz_places.visit_count from moz_places;"
    cursor.execute(select_statement)

    data = cursor.fetchall()

    g = nx.Graph()

    wikiList = []
    linkList = []
    n = 0

    limit = 60000

    from os import read
    from pathlib import Path

    #read json file
    filename = str(Path.cwd()) + "\graph.json"
    print(filename)
    with open(filename) as f:
        in_graph = json.load(f)

    article_titles = in_graph["nodes"]
    article_titles = [title["id"] for title in article_titles]

    print(len(article_titles))

    start_time = time.time()
    repeats = 0

    for entry in reversed(data):
        if("wikipedia.org" in entry[0]):
            try:
                n = n + 1
                #print(entry[0])
                search = wikipedia.search(extractTitle(entry[0]))
                if(search[0] == "Young British Artists"):
                    break
                #print(search)
                title = search[0]
                if(title not in wikiList):
                    wikiList.append(title)
                    g.add_node(title)
                    print(title)
            except:
                print(entry[0])

        if(n >= limit):
            break

    #print(wikiList)
    print("wikilist done")
    print(time.time() - start_time)
    print(n)

    start_time = time.time()

    n = 0

    for entry in article_titles:
        try:
            n = n + 1
            page = pageSearch(entry)

            for link in page.links:
                if(link in article_titles):
                    print(entry + " --> " + link)
                    g.add_edge(entry, link)

                    if(n >= limit):
                        break
        except:
            print("exception")

   # n = 0
   # for entry in linkList:
   #     n = n + 1
   #     for subEntry in entry:
   #         if(subEntry in wikiList and ("stats" not in subEntry)):
   #             print(wikiList[n] + " --> " + subEntry)
   #             g.add_edge(str(wikiList[n]), str(subEntry))

    data = json_graph.node_link_data(g)
    with open('graph2.json', 'w') as f:
        json.dump(data, f, indent=4)

def extractTitle(url):
    try:
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features='lxml')

        out = soup.find('h1')
        if(out.string is None):
            return str(url)
        return out.string
    except:
        return str(url)

def pageSearch(entry):
    try:
        return wikipedia.page(entry, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as e:
        print(e)

graphFunc()
