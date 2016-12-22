import networkx as nx
import pandas as pd
import numpy as np

FILE_NETWORK_RETWEET_WEIGHT = "higgs-retweet_network.edgelist"

data = pd.read_csv(FILE_NETWORK_RETWEET_WEIGHT, sep=' ', names = ['source', 'target','weight'])

G = nx.DiGraph()

for idx,row in data.iterrows():
    G.add_edge(row['target'], row['source'], weight= row['weight'])

#katz_centrality = nx.katz_centrality(G, max_iter=10000)
pagerank = nx.pagerank(G)

df = pd.DataFrame(list(pagerank.items()), columns=['node','pagerank'])

df.to_csv('page_rank.csv', index = False)
