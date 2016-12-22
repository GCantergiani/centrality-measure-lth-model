import networkx as nx
import pandas as pd
import numpy as np

FILE_NETWORK_RETWEET_WEIGHT = "higgs-retweet_network.edgelist"

data = pd.read_csv(FILE_NETWORK_RETWEET_WEIGHT, sep=' ', names = ['source', 'target','weight'])

G = nx.DiGraph()

for idx,row in data.iterrows():
    G.add_edge(row['target'], row['source'], weight= row['weight'])

katz_centrality = nx.katz_centrality_numpy(G)
#katz_centrality = nx.katz_centrality(G, max_iter=200000)

df = pd.DataFrame(list(katz_centrality.items()), columns=['node','katz_centrality'])

df.to_csv('katz_centrality_numpy.csv', index = False)
