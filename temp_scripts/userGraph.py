#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dprydereid@gmail.com
#11/03/22

## INPUT: user log json file with one log per line
# OUTPUT: 1) .png graph of the transitions between hardware states.  
#       2) An adjacency matrix for the user graph - this will allow comparison between user graphs
#       3) Basic graph data as a csv file

import json
import math
from re import X
#import numpy as np
import pandas as pd
import argparse
#from matplotlib import cm
#import matplotlib.pyplot as plt
from pathlib import Path
import networkx as nx
# import netcomp as nc
# import pygraphviz as pgv
from pyvis.network import Network



parser = argparse.ArgumentParser(description='Read JSON data file of logging data.')
parser.add_argument('--input', dest='input_file', type=str, help='the name of the datafile to read from')
parser.add_argument('--out', dest='out_dir', type=str, help='the name of the directory to output files to')
                

args = parser.parse_args()
input = args.input_file
out = args.out_dir

G = nx.MultiDiGraph()       #Multigraph for creating full number of edges on a graph including self loops
H = nx.DiGraph()               # Above graph will be used to create a non-multi edged graph, but with weighted edges inversely proportional to the edge count


# The number of nodes is fixed and consists of the hardware modes possible.
# Nodes will be sized later based upon the degree of the node (in or out?)
G.add_node('voltage_step', shape='circle', color="blue", height=0.1)
G.add_node('voltage_ramp', shape='circle', color="blue", height=0.1)
G.add_node('position_step', shape='circle', color="blue", height=0.1)
G.add_node('position_ramp', shape='circle', color="blue", height=0.1)
G.add_node('speed_step', shape='circle', color="blue", height=0.1)
G.add_node('speed_ramp', shape='circle', color="blue", height=0.1)

## Get all the hardware commands sent by this user and store in an array
command_array = []

with open(input) as f:
    lines = f.readlines()
    for line in lines:
        if len(line)>1:
            try:
                log_data = json.loads(line)
                #command sent
                if(log_data["payload"]["log"] == 'voltage'):
                    command_array.append('voltage_step')
                elif(log_data["payload"]["log"] == 'voltage_ramp'):
                    command_array.append('voltage_ramp')
                elif(log_data["payload"]["log"] == 'position'):
                    command_array.append('position_step')
                elif(log_data["payload"]["log"] == 'position_ramp'):
                    command_array.append('position_ramp')
                elif(log_data["payload"]["log"] == 'speed'):
                    command_array.append('speed_step')
                elif(log_data["payload"]["log"] == 'speed_ramp'):
                    command_array.append('speed_ramp')
                else:
                    pass

            except:
                pass

#Created a directed multigraph of all edges, including self loops
for index, command in enumerate(command_array):
    if(index + 1 < len(command_array)):
        G.add_edge(command, command_array[index+1], color='black')
            
edge_dict = {} # {edge: count, .....}
for edge in nx.edges(G):
    if(edge in edge_dict.keys()):
        edge_dict[edge] += 1
    else:
        edge_dict[edge] = 1


## Hexagonal layout of nodes
H.add_node('voltage_step', shape='circle', color="blue", height=0.01, physics=False, x=100, y=-200*math.sin(math.pi/3))
H.add_node('voltage_ramp', shape='circle', color="blue", height=0.01, physics=False, x=-100, y=-200*math.sin(math.pi/3))
H.add_node('position_step', shape='circle', color="blue", height=0.01, physics=False, x=200, y=0)
H.add_node('position_ramp', shape='circle', color="blue", height=0.01, physics=False, x=-200, y=0)
H.add_node('speed_step', shape='circle', color="blue", height=0.01, physics=False, x=100, y=200*math.sin(math.pi/3))
H.add_node('speed_ramp', shape='circle', color="blue", height=0.01, physics=False, x=-100, y=200*math.sin(math.pi/3))

edge_list = list(edge_dict.keys())
#print(edge_list)
H.add_edges_from(edge_list)
#print(H.edges())
nx.set_edge_attributes(H, name="weight", values=edge_dict)

pen_dict = {}
for edge in edge_dict.keys():
    pen_dict[edge] = max(0, min(edge_dict[edge], 20))
nx.set_edge_attributes(H, name="penwidth", values=pen_dict)
nx.set_edge_attributes(H, name="label", values=edge_dict)
#print(H.edges())
#print(nx.get_edge_attributes(H, 'weight'))

## 1) OUTPUT - .png image of graph =================================================================
## .html graph for each user

username = Path(input).stem
## Centrality measures - get the centrality measure for each node
#deg_cent = nx.degree_centrality(G)      #deg centrality of original multigraph
#eigen_cent = nx.eigenvector_centrality(G)

# Change the size of each node depending on its centrality measure
# H.node['voltage_step']['height'] = max(0, min(deg_cent['voltage_step'], 10))
# H.node['voltage_ramp']['height'] = max(0, min(deg_cent['voltage_ramp'], 10))
# H.node['position_step']['height'] = max(0, min(deg_cent['position_step'], 10))
# H.node['position_ramp']['height'] = max(0, min(deg_cent['position_ramp'], 10))
# H.node['speed_step']['height'] = max(0, min(deg_cent['speed_step'], 10))
# H.node['speed_ramp']['height'] = max(0, min(deg_cent['speed_ramp'], 10))
# Draw graph
#A = nx.nx_agraph.to_agraph(H)
#A.layout(prog='dot')
#A.draw('%s/%s-graph.png' % (out, username))
g=Network(height=800,width=800,notebook=False, directed=True)
#g.toggle_hide_edges_on_drag(False)
#g.barnes_hut()
g.from_nx(H)
g.set_options("""
    var options = {
  "nodes": {
    "font": {
      "color": "rgba(255,255,255,1)"
    }
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "physics": {
    "minVelocity": 0.75
  }
}
 """)
## g.show_buttons()
g.save_graph('%s/%s-graph.html' % (out,username))


## 2) OUTPUT - adjacency matrix =================================================================

## for comparison of graphs with netcomp need to convert to adjaceny matrices
A1 = nx.to_pandas_adjacency(H)
A1.to_csv('%s/%s-graph-adjacency.csv' % (out, username))



## 3) OUTPUT - graph data to .csv =================================================================
## Graph data to save - centrality of each node, edges and weights, in and out degree of each node
N, K, deg = G.order(), G.size(), G.degree()
avg_deg = float(K)/N
d = {'Order':N, 'Size':K, 'Degree':deg, 'Avg degree':avg_deg}
df = pd.DataFrame(data=d)
df.to_csv('%s/%s-graph-data.csv' % (out, username))





