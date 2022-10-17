
# dprydereid@gmail.com
#18/03/22

# Module specifcying different distance measures for two graphs

# 1. DeltaCon distance between graphs of known node structure

import networkx as nx
import netcomp as nc
import numpy as np

def deltaConFromGraph(G1, G2):
        """Returns the deltaCon distance between two graphs. Returns a distance value, not a similarity.

        Parameters:
        G1 (NetworkX graph): A NetworkX graph object
        G2 (NetworkX graph): A NetworkX graph object

        Returns:
        float: DeltaCon distance
        """
        A1 = nx.adjacency_matrix(G1)
        A2 = nx.adjacency_matrix(G2)
        dist = nc.deltacon0(A1,A2)
        return dist

def deltaConFromAdjacency(A1, A2):
        """Returns the deltaCon distance between two adjacency matrices. Returns a distance value, not a similarity.

        Parameters:
        A1 (array): An adjacency matrix as an array
        A2 (array): An adjacency matrix as an array

        Returns:
        float: DeltaCon distance
        """
        dist = nc.deltacon0(A1,A2)
        return dist

def distanceMatrixDeltaConFromGraph(graph_list):
        distance_matrix = []
        for g in graph_list:
                g_dist = []
                for h in graph_list:
                        g_dist.append(deltaConFromGraph(g, h))

                distance_matrix.append(g_dist)
        
        return distance_matrix

def distanceMatrixDeltaConFromAdjacency(adjacency_list):
    distance_matrix = []
    for g in adjacency_list:
        g_dist = []
        for h in adjacency_list:
            g_dist.append(deltaConFromAdjacency(g, h))

        distance_matrix.append(g_dist)
    
    return distance_matrix


# 2. Graph Edit distance

"""Returns the Graph Edit Distance (GED) between two adjacency matrices. Returns a distance value, not a similarity.

        Parameters:
        A1 (array): An adjacency matrix as an array
        A2 (array): An adjacency matrix as an array

        Returns:
        float: GED distance
"""
def GEDfromAdjacency(A1, A2):
    diff = A1 - A2
    diff_abs = np.abs(diff)
    return np.sum(diff_abs)


# 3. Edge distance

def EdgeExists(weight):
    if weight > 0:
        return 1
    else:
        return 0

"""Returns the 'edge distance' between two adjacency matrices. Returns a distance value, not a similarity.

        Parameters:
        A1 (array): An adjacency matrix as an array
        A2 (array): An adjacency matrix as an array

        Returns:
        float: edge distance
"""
def EdgeDistanceAdjacency(A1, A2):
    edge_exists = np.vectorize(EdgeExists)
    A1_converted = edge_exists(A1)
    A2_converted = edge_exists(A2)
    diff = A1_converted - A2_converted
    diff_abs = np.abs(diff)
    return np.sum(diff_abs)

"""Returns the 'signed edge distance' between two adjacency matrices. Returns a distance value, not a similarity.

        Parameters:
        A1 (array): An adjacency matrix as an array. Adjacency matrix to compare.
        A2 (array): An adjacency matrix as an array. Adjacency matrix to compare to. The expert model.

        Returns:
        int[]: [e+, e-, e_max] -> where e+ is the number of additional edges, e- the number of missing edges, e_max is the number of edges in A2
"""
def SignedEdgeDistanceAdjacency(A1, A2):
    A1_np = np.asarray(A1)
    A2_np = np.asarray(A2)
    
    edge_exists = np.vectorize(EdgeExists)
    A1_converted = edge_exists(A1_np)
    A2_converted = edge_exists(A2_np)
    e_max = np.sum(A2_converted)
    diff = A1_converted - A2_converted
    c_p = np.count_nonzero(diff == 1)
    c_n = np.count_nonzero(diff == -1)
    return [c_p, c_n, e_max]



## Custom distance - edge weighted deltaCon
## (10*e-/emax + 1)*DC
def edgeWeightedDCFromAdjacency(A1,A2):
    dc = deltaConFromAdjacency(A1,A2)
    edge_dist = SignedEdgeDistanceAdjacency(A1,A2)
    
    return (10*edge_dist[1]/edge_dist[2] + 1)*dc
    


def distanceMatrixEdgeWeightedDCFromAdjacency(adjacency_list):
    distance_matrix = []
    for g in adjacency_list:
        g = np.asarray(g)
        g_dist = []
        for h in adjacency_list:
            h = np.asarray(h)
            g_dist.append(edgeWeightedDCFromAdjacency(g, h))

        distance_matrix.append(g_dist)
    
    return distance_matrix