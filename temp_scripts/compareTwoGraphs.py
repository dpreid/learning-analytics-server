#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dprydereid@gmail.com
#29/04/22

# Compare two graphs of known and equal nodes.

#INPUT: Two adjacency matrices, representing each graph.
# OUTPUT: Similarity rating into a csv file - append comparison to file with user name + distance measure + evaluation of similarity?


from graphCompare import EdgeDistanceAdjacency, GEDfromAdjacency, SignedEdgeDistanceAdjacency, deltaConFromAdjacency
import argparse
import pandas as pd
from pathlib import Path

import os
import sys
sys.path.append('/home/david/graph-comp')
from TaskDistance import TaskDistance # type: ignore
from distances import GED, euclidean, canberra, weighted_jaccard # type: ignore

parser = argparse.ArgumentParser(description='Read .csv files for user graph adjacency matrices.')
parser.add_argument('--graph1', dest='g1', type=str, help='adjacency matrix of graph 1 as csv')
parser.add_argument('--graph2', dest='g2', type=str, help='adjacency matrix of graph 2 as csv')
parser.add_argument('--out', dest='out', type=str, help='directory to output comparison file to')

args = parser.parse_args()
g1 = args.g1
g2 = args.g2
out = args.out

ad1 = pd.read_csv(g1, index_col=0).to_numpy()
ad2 = pd.read_csv(g2, index_col=0).to_numpy()

#delta con distance
dist_dc = deltaConFromAdjacency(ad1,ad2)     #unbounded

#GED distance
dist_ged = GED(ad1,ad2)

#Simple edge distance
#g_distance_edge = EdgeDistanceAdjacency(ad1,ad2)

#Signed edge distance
#g_distance_edge_signed = SignedEdgeDistanceAdjacency(ad1,ad2)
#e_max = g_distance_edge_signed[2]

#distance = (10.0*g_distance_edge_signed[1]/e_max + 1)*g_distance      # Custom distance metric

dist_euc = euclidean(ad1,ad2)
dist_can = canberra(ad1,ad2)
dist_jac = weighted_jaccard(ad1,ad2)

taskDistance = TaskDistance(pd.DataFrame(ad1),pd.DataFrame(ad2),10,1)
## different models of task distance

taskDistance_tuned = TaskDistance(pd.DataFrame(ad1),pd.DataFrame(ad2),12,1,1,2,-1)
taskDistance_missingweighted = TaskDistance(pd.DataFrame(ad1),pd.DataFrame(ad2),12,0,1,2,-1)
taskDistance_exploration = TaskDistance(pd.DataFrame(ad1),pd.DataFrame(ad2),0,10,2,2,-1)



index = Path(g1).stem.index('graph') - 1
username = Path(g1).stem[0:index]
data = [{"graph1": username, "graph2": Path(g2).stem, "delta_con": dist_dc, "ged": dist_ged, "euclidean": dist_euc, "canberra": dist_can, "weighted_jaccard": dist_jac, 
        "taskdistance": taskDistance, 
        "taskdistance_tuned": taskDistance_tuned,
        "taskdistance_missingweighted": taskDistance_missingweighted,
        "taskdistance_exploration": taskDistance_exploration
        }]

df = pd.DataFrame(data=data)
if(os.path.exists('%s/graph-comparisons.csv' % out)):
    df.to_csv('%s/graph-comparisons.csv' % out, mode='a', header=None)
else:
    df.to_csv('%s/graph-comparisons.csv' % out, mode='w', header=True)

