import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
import networkx as nx
import itertools
import sqlite3
from forcenetwork import DrawNetGraph


con = sqlite3.connect("data.sqlite")

auth_docu_mod ='''
select authors_id, documents_id, full_name, title
from authors a, documents b, documents_authors c
where a.id=c.authors_id and c.documents_id=b.id;
'''

X = pd.read_sql(auth_docu_mod, con)

Documents = X.documents_id.groupby(by = X.documents_id).size()

Authors = X.groupby(by = X.authors_id).size()

Y = X["documents_id"].unique()
all_authors = set(X.authors_id)

x = []
y = {}
uniq = Y

for article in uniq:
    y[article] = X.loc[X['documents_id'] == article]['authors_id']

combinations = []
for article in y:
    g = list(itertools.combinations(y[article], 2))
    for sub in g:
        combinations.append(sub)

suc_authors = set()
for edge in combinations:
    for auth in edge:
        suc_authors.add(auth)

single_dogs= all_authors - suc_authors

A_N = X[['authors_id', 'full_name']]
A_N = A_N.drop_duplicates()
A_N.index = A_N.authors_id


SA_paper_num = Authors.ix[single_dogs]
Single_Auth = A_N[A_N.authors_id.isin(single_dogs)]
Single_Auth['paper_num'] = SA_paper_num

SuA_paper_num = Authors.ix[suc_authors]
Success_Auth = A_N[A_N.authors_id.isin(suc_authors)]
Success_Auth['paper_num'] = SuA_paper_num

Edges = Series(combinations)
Edges = Edges.groupby(Edges).size().reset_index()
Edges.rename(columns = {0: 'frequency', "index" : 'Edge'}, inplace = True)


First_Blood = nx.Graph()
for i in range(len(Single_Auth)):
    a = Single_Auth.iloc[i]
    First_Blood.add_node(a.authors_id, full_name =a.full_name, paper_num = a.paper_num)

G = nx.Graph()
for i in range(len(Success_Auth)):
    a = Success_Auth.iloc[i]
    G.add_node(a.authors_id, full_name =a.full_name, paper_num = a.paper_num)

for i in range(len(Edges)):
    edge = Edges.iloc[i]
    G.add_edge(edge.Edge[0], edge.Edge[1], freq = edge.frequency)

subgraphs = list(nx.connected_component_subgraphs(G))

subgraphs_size = Series()
length = len(subgraphs)
for i in range(length):
    subgraphs_size.loc[i] = len(subgraphs[i].nodes())


double_kill = [ subg for subg in subgraphs if len(subg.nodes()) == 2 ]
triple_kill = [ subg for subg in subgraphs if len(subg.nodes()) == 3 ]
quadra_kill = [ subg for subg in subgraphs if len(subg.nodes()) == 4 ]

penta_kill  = [ subg for subg in subgraphs
               if len(subg.nodes()) == 5  or len(subg.nodes()) == 6 ]

rampage     = [ subg for subg in subgraphs
               if len(subg.nodes()) == 7  or len(subg.nodes()) == 8 ]

godlike     = [ subg for subg in subgraphs
               if len(subg.nodes()) >= 10 and len(subg.nodes()) < 14]

legendary   = [ subg for subg in subgraphs
               if len(subg.nodes()) >= 14 ]


Double_Kill = nx.Graph()
for subg in double_kill:
    Double_Kill.add_edges_from(subg.edges(data = True))
    Double_Kill.add_nodes_from(subg.nodes(data = True))


Triple_Kill = nx.Graph()
for subg in triple_kill:
    Triple_Kill.add_edges_from(subg.edges(data = True))
    Triple_Kill.add_nodes_from(subg.nodes(data = True))

Quadra_Kill = nx.Graph()
for subg in quadra_kill:
    Quadra_Kill.add_edges_from(subg.edges(data = True))
    Quadra_Kill.add_nodes_from(subg.nodes(data = True))

Penta_Kill = nx.Graph()
for subg in penta_kill:
    Penta_Kill.add_edges_from(subg.edges(data = True))
    Penta_Kill.add_nodes_from(subg.nodes(data = True))

Rampage = nx.Graph()
for subg in rampage:
    Rampage.add_edges_from(subg.edges(data = True))
    Rampage.add_nodes_from(subg.nodes(data = True))

Godlike = nx.Graph()
for subg in godlike:
    Godlike.add_edges_from(subg.edges(data = True))
    Godlike.add_nodes_from(subg.nodes(data = True))

Legendary = nx.Graph()
for subg in legendary:
    Legendary.add_edges_from(subg.edges(data = True))
    Legendary.add_nodes_from(subg.nodes(data = True))



DrawNetGraph(First_Blood, "Graphs/1_first")
DrawNetGraph(Double_Kill, "Graphs/2_double")
DrawNetGraph(Triple_Kill, "Graphs/3_triple")
DrawNetGraph(Quadra_Kill, 'Graphs/4_quadra')
DrawNetGraph(Penta_Kill, "Graphs/4_penta")
DrawNetGraph(Rampage, "Graphs/5_rampage")
DrawNetGraph(Godlike, "Graphs/6_godlike")
DrawNetGraph(Legendary,"Graphs/7_legendary")
