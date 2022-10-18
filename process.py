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
"""
Takes a new log message and adds it to the appropriate user log file
message is already in json format and been loaded into json previously
"""
def AddUserLog(message):
    try:
        user = message["user"]
        exp = message["exp"]
        filename = '%s-%s.json' % (user, exp)

        with open('/app/' + filename, 'a') as outfile:
            d = json.dumps(message)
            outfile.write(d)
            outfile.write('\n')
        
    except:
        pass

"""
Creates a visual representation of a user graph from a user adjacency matrix
"""
def GenerateGraph(user, exp):
    
    return


"""
Converts a user log file into a adjacency matrix

If the matrix already exists, then it adds the log file to that matrix.
"""
def GenerateAdjacencyMatrix(user, exp):
    command_array = GetCommandList(user, exp)

    if(exp == "spinner"):
        nodes = ['voltage_step', 'voltage_ramp', 'position_step', 'position_ramp', 'speed_step', 'speed_ramp']
    else:
        nodes = []

    zero = np.zeros(shape=(len(nodes), len(nodes)))
    df = pd.DataFrame(zero, nodes, nodes)

    ## add additional weight to 
    for index, command in enumerate(command_array):
        if(index + 1 < len(command_array)):
            df[command][command_array[index+1]] += 1

    df.to_csv('%s-%s-adjacency.csv' % (user, exp))
    return

"""
Generates a list of student commands from the user log file
Returns and array of commands sent to hardware
"""
def GetCommandList(user, exp):
    return []

"""
Creates the base graph for the spinner experiment.
"""
def CreateEmptySpinnerGraph():
    return 

"""
Creates the base graph for the pendulum experiment.
"""
def CreateEmptyPendulumGraph():
    return 