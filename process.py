#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
process.py

Methods for processing student log data. 

Generates log files for recent student logging via UI.
Generates graphs from log files and adds new log file data to graphs.
Generates student adjacency matrices and graph (SVGs).

@author: dprydereid@gmail.com
"""
import pandas as pd
import numpy as np
import networkx as nx
import json
import os
import math
import matplotlib.pyplot as plt
from pyvis.network import Network

data_dir = "./test/data"

"""
Takes a new log message and adds it to the appropriate user log file
message is already in json format and been loaded into json previously
"""
def AddUserLog(message):
    try:
        user = message["user"]
        exp = message["exp"]
        filename = '%s-%s.json' % (user, exp)

        with open('%s/%s' % (data_dir, filename), 'a') as outfile:
            d = json.dumps(message)
            outfile.write(d)
            outfile.write('\n')
        
    except:
        pass

"""
Creates a visual representation of a user graph from a user adjacency matrix

Returns a graph representing student data or an empty graph if no data is present.
"""
def GenerateGraph(user, exp):
    
    if(os.path.isfile('%s/%s-%s-adjacency.csv' % (data_dir, user, exp))):
        df = pd.read_csv('%s/%s-%s-adjacency.csv' % (data_dir, user, exp), index_col=0)
        G = nx.from_pandas_adjacency(df, create_using=nx.DiGraph)
    else:
        G = nx.DiGraph()
    
    return G


def SaveGraphHTML(user, exp):
    
    G = GenerateGraph(user, exp)
    G = SetGraphProperties(G, 'spinner')
    #print(G.edges(data=True))
    g=Network(height=800,width=800,notebook=False, directed=True)
    g.from_nx(G)
    # g.set_options("""
    #     var options = {
    # "nodes": {
    #     "font": {
    #     "color": "rgba(0,0,0,1)"
    #     }
    # },
    # "edges": {
    #     "color": {
    #     "inherit": true
    #     },
    #     "smooth": {
    #         "forceDirection": "none",
    #         "roundness": 1
    # }
    # },
    # "physics": {
    #     "minVelocity": 0.75
    # }
    # }
    # """)
    g.show_buttons()
    g.save_graph('%s/%s-%s-graph.html' % (data_dir, user, exp))

def GetGraphComponents(user, exp):
    
    G = GenerateGraph(user, exp)
    G = SetGraphProperties(G, exp)
    #print(G.edges(data=True))
    g=Network(height=800,width=800,notebook=False, directed=True)
    g.from_nx(G)
    
    nodes, edges, heading, height, width, options = g.get_network_data()
    
    return nodes, edges

def GetComparisonGraphComponents(comparison, exp):
    print('doing')
    df = pd.read_csv('./comparison_graphs/%s.csv' % comparison, index_col=0)
    G = nx.from_pandas_adjacency(df, create_using=nx.DiGraph)
    G = SetGraphProperties(G, exp)
    #print(G.edges(data=True))
    g=Network(height=800,width=800,notebook=False, directed=True)
    g.from_nx(G)
    
    nodes, edges, heading, height, width, options = g.get_network_data()
    
    return nodes, edges


def DrawGraphImage(user, exp):
    
    G = GenerateGraph(user, exp)

    if(exp == "spinner"):
        edge_labels = dict([((u,v), d['weight']) for u,v,d in G.edges(data=True)])
        pos = {'voltage_step': [100,200*math.sin(math.pi/3)], 'voltage_ramp': [-100, 200*math.sin(math.pi/3)], 'position_step': [200, 0], 'position_ramp': [-200, 0], 'speed_step': [100, -200*math.sin(math.pi/3)], 'speed_ramp': [-100, -200*math.sin(math.pi/3)]}
    
    else:
        edge_labels = dict()
        pos = nx.spring_layout(G)
    
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels, label_pos=0.25, font_size=10)
    #nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.15', node_size=800)
    nx.draw(G, pos, with_labels=True)
    plt.show()


"""
Converts a user log file into a adjacency matrix

If the matrix already exists, then it adds the log file to that matrix.

Once the matrix is updated it will delete the log file
"""
def GenerateAdjacencyMatrix(user, exp, deleteLogFile = True):
    command_array, last_line = GetCommandList(user, exp)

    if(exp == "spinner"):
        nodes = ['voltage_step', 'voltage_ramp', 'position_step', 'position_ramp', 'speed_step', 'speed_ramp']
    else:
        nodes = []

    # if an adjacency matrix for a user already exists, then add new data to that
    if(os.path.isfile('%s/%s-%s-adjacency.csv' % (data_dir, user, exp))):
        df = pd.read_csv('%s/%s-%s-adjacency.csv' % (data_dir, user, exp), index_col=0)
    else:
        matrix = np.zeros(shape=(len(nodes), len(nodes)))
        df = pd.DataFrame(matrix, nodes, nodes)

    ## add additional weight to the adjacency matrix
    ## this order of the rows and columns is necessary to get the correct direction on graphs when drawing a graph
    for index, command in enumerate(command_array):
        if(index + 1 < len(command_array)):
            df[command_array[index+1]][command] += 1

    # output the updated csv to file
    df.to_csv('%s/%s-%s-adjacency.csv' % (data_dir, user, exp))

    # for storage reasons do not store the complete json log list
    # need to maintain the latest command however to generate the correct edge for the next mode set
    if(os.path.isfile('%s/%s-%s.json' % (data_dir, user, exp)) and deleteLogFile):
        os.remove('%s/%s-%s.json' % (data_dir, user, exp))
        with open('%s/%s-%s.json' % (data_dir, user, exp), 'a') as f:
            f.write(last_line)

    return df

"""
Generates a list of student commands from the user log file
Returns and array of commands sent to hardware
Also returns the last line of the command list for storage
"""
def GetCommandList(user, exp):
    command_array = []
    last_line = ''
    if(os.path.isfile('%s/%s-%s.json' % (data_dir, user, exp))):
        with open('%s/%s-%s.json' % (data_dir, user, exp)) as f:
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
            last_line = line
    
    return command_array, last_line


def SetGraphProperties(G, exp):
    
    if(exp == 'spinner'):
        x = {'voltage_step': 100, 'voltage_ramp': -100, 'position_step': 200, 'position_ramp': -200, 'speed_step': 100, 'speed_ramp': -100 }
        y = {'voltage_step': -200*math.sin(math.pi/3), 'voltage_ramp': -200*math.sin(math.pi/3), 'position_step': 0, 'position_ramp': 0, 'speed_step': 200*math.sin(math.pi/3), 'speed_ramp': 200*math.sin(math.pi/3)}
        nx.set_node_attributes(G, x, 'x')
        nx.set_node_attributes(G, y, 'y')

        #make sure physics doesn't shift the positions
        nx.set_node_attributes(G, False, name='physics')

        #ensure graph has labels of edge weights.
        edge_labels = dict([((u,v), str(int(d['weight']))) for u,v,d in G.edges(data=True)])
        nx.set_edge_attributes(G, edge_labels, name='label')

    return G