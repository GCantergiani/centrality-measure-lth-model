import networkx as nx
import pandas as pd
import numpy as np

FILE_NETWORK_RETWEET_WEIGHT = "higgs-retweet_network.edgelist"

data = pd.read_csv(FILE_NETWORK_RETWEET_WEIGHT, sep=' ', names = ['source', 'target','weight'])

G = nx.DiGraph()

for idx,row in data.iterrows():
    G.add_edge(row['target'], row['source'], weight= row['weight'])

dgc = nx.betweenness_centrality(G)


df = pd.DataFrame(list(dgc.items()), columns=['node','degree'])

df.to_csv('betweenness_centrality.csv', index = False)
