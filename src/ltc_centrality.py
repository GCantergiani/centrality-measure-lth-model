import networkx as nx
import pandas as pd
import sys
import numpy as np

FILE_NETWORK_RETWEET_WEIGHT = "./higgs-retweet_network.edgelist"
ALERNATIVE_BOOSTRAP_NEIGHBORS_ELECTION = False
PRINT_STEPS = True

def generate_graph():

    df_retweets = pd.read_csv(FILE_NETWORK_RETWEET_WEIGHT, sep=' ', names = ['source', 'target','weight'])

    # Create first directed graph
    G1 = nx.DiGraph()
    for idx,row in df_retweets.iterrows():
        G1.add_edge(row['target'], row['source'], weight= row['weight'])

    # Create second directed graph
    G2 = nx.DiGraph()
    for idx,row in data.iterrows():
        G2.add_edge(row['source'], row['target'], weight= row['weight'])    

    return G1, G2


def add_plurality_attribute(G1, G2, nodes):

    for n in nodes:
        
        if(G1.in_degree(n) == 0):
            plurality = sys.maxsize
        else:
            sum_weight = 0
            for g2_node_source in G2.neighbors(n):
                sum_weight = sum_weight + G1.get_edge_data(g2_node_source,n)['weight']

            plurality = int(sum_weight/2) + 1
            
        G1.node[n]['plurality'] = plurality

    return G1


def write_result(nodes, df_ltc):

    df_centrality = pd.DataFrame(nodes, columns=["node"])
    df_centrality["lineal_threshold"] = df_ltc

    df_centrality.to_csv('lineal_threshold_centrality_retweets.csv', index = False)


def main():

    unique_nodes = []
    lineal_threshold_to_pandas = []

    # Read graphs
    G1, G2 = generate_graph()
    
    for node in G1.nodes_iter():
        unique_nodes.append(node)
    
    # Remove duplicates nodes
    unique_nodes = list(set(unique_nodes))

    # Add plurality attribute
    G1 = add_plurality_attribute(G1, G2, unique_nodes)

    # For each unique nodes
    for idx, n in enumerate(unique_nodes):

        if PRINT_STEPS:
            print('Node: {0}'.format(n))
        
        
        first_step_per_node = True
        
        nodes_to_add_group = []
        
        neighbors = []

        if(ALERNATIVE_BOOSTRAP_NEIGHBORS_ELECTION):
            neighbors.extend(G1.neighbors(n))
        else:
            neighbors.extend(G1.neighbors(n))
            neighbors.extend(G2.neighbors(n))
        
        group = []
        
        group.append(n)
        group.extend(neighbors)

        if PRINT_STEPS:
            print('I: 0 ; Neighbors: {0} ; count: {1}'.format(neighbors, len(neighbors)))
        
        depth_level = 0

        while( first_step_per_node or (len(nodes_to_add_group) >= 1) ):
            
            first_step_per_node = False
            
            neighbors.extend(nodes_to_add_group)
            group.extend(nodes_to_add_group)
            
            nodes_to_add_group = []
        
            if PRINT_STEPS:
                print('\t neighbors: {1}'.format(n, neighbors))

            dispersion = []

            vei = []
            for v in neighbors:
                vei.extend(G1.neighbors(v))

            dispersion = list(set(vei) - set(group))

            if PRINT_STEPS:
                print('\t dispersion {0} '.format(dispersion))

            for n_sub_level in dispersion:
                plurality = G1.node[n_sub_level]['plurality']
                
                if PRINT_STEPS:
                    print('\t \t Reach node {0} | plurality {1}'.format(n_sub_level,plurality))

                group_influce = 0
                for node_group in group:
                    if(G1.get_edge_data(node_group,n_sub_level)):
                        group_influce = group_influce + G1.get_edge_data(node_group,n_sub_level)['weight']

                if PRINT_STEPS:
                    print('\t \t group {0} | influce {1}'.format(group, group_influce))

                if(group_influce >= plurality):
                    nodes_to_add_group.append(n_sub_level)

            if PRINT_STEPS:
                print('\t \t \t new group {0} '.format(nodes_to_add_group))
                print('{0} ; {1} ; {2}'.format(n, depth_level, len(neighbors)))
                print()

            depth_level = depth_level +1 
            

        lineal_threshold_to_pandas.append(len(neighbors) + 1)


    write_result(unique_nodes, lineal_threshold_to_pandas)


if __name__ == "__main__":
    main()