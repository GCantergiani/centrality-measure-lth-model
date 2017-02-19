#!/usr/local/bin/python3

# A template to calculate centrality measures using networkX and Pandas.
# The list of supported algorithms can be seen in:
# - http://networkx.readthedocs.io/en/stable/reference/algorithms.html

import networkx as nx
import pandas as pd
import numpy as np

FILE_NETWORK_RETWEET_WEIGHT = "higgs-retweet_network.edgelist"

def main():

	data = pd.read_csv(FILE_NETWORK_RETWEET_WEIGHT, sep=' ', names = ['source', 'target','weight'])

	# Create a directed graph
	G = nx.DiGraph()

	# We change the direction to create a new graph.
	for idx,row in data.iterrows():
	    G.add_edge(row['target'], row['source'], weight= row['weight'])

	# Here we choose the algorithm, for example pagerank calculation
	pagerank = nx.pagerank(G)

	# Create a dataframe with the results
	df = pd.DataFrame(list(pagerank.items()), columns=['node','pagerank'])

	# Write dataframe as a csv file
	df.to_csv('page_rank.csv', index = False)


if __name__ == "__main__":
    main()