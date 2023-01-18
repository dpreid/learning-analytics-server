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
import glob
import json
import math
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import pandas as pd
from pyvis.network import Network

data_dir = os.environ.get("DATA_PATH", "./test/data")
comp_graph_dir = os.environ.get("COMP_PATH", "./comparison_graphs")

"""
Takes a new log message and adds it to the appropriate user log file
message is already in json format and been loaded into json previously
"""
def AddUserLog(message):
    try:
        user = message["user"]
        exp = message["exp"]
        hardware = message["hardware"]
        course = message['course']
        filename = '%s-%s-%s-%s.json' % (user, hardware, exp, course)

        with open('%s/%s' % (data_dir, filename), 'a') as outfile:
            d = json.dumps(message)
            outfile.write(d)
            outfile.write('\n')
        
    except:
        pass

"""
Takes a new log message and adds it to the appropriate user log file
message is already in json format and been loaded into json previously
"""
def AddUserFeedback(message):
    try:
        
        user = message["user"]
        exp = message["exp"]
        course = message['course']
        filename = '%s-%s-%s-feedback.csv' % (user, exp, course)
        new_state = message['payload']['state']
        new_subject = message['payload']['subject']
        
        # if an adjacency matrix for a user already exists, then add new data to that
        if(os.path.isfile('%s/%s' % (data_dir, filename))):
            df = pd.read_csv('%s/%s' % (data_dir, filename), index_col=0)
        else:
            states = ['Engaged', 'Curious', 'Delighted', 'Bored', 'Confused', 'Frustrated', 'Surprised', 'Anxious']
            subjects = ['Workbook', 'Remote work', 'Hardware', 'UI', 'LA', 'Other']
            if(course == 'cie3'):
                subjects.append('spinner-cie3-1-2')
                subjects.append('spinner-cie3-3')
                subjects.append('spinner-cie3-4')
            elif(course == 'engdes1'):
                subjects.append('pendulum-engdes1-1')
                subjects.append('pendulum-engdes1-2')
            
            matrix = np.zeros(shape=(len(states), len(subjects)))
            df = pd.DataFrame(matrix, states, subjects)
            
        df[new_subject][new_state] += 1
        df.to_csv('%s/%s' % (data_dir, filename))
        
    except:
        print('error adding feedback')
        pass

"""
Creates a visual representation of a user graph from a user adjacency matrix

Returns a graph representing student data or an empty graph if no data is present.
"""
def GenerateGraph(user, exp, course):
    filename = '%s-%s-%s-adjacency.csv' % (user, exp, course)
    if(os.path.isfile('%s/%s' % (data_dir, filename))):
        df = pd.read_csv('%s/%s' % (data_dir, filename), index_col=0)
        G = nx.from_pandas_adjacency(df, create_using=nx.DiGraph)
    else:
        G = nx.DiGraph()
    
    return G


## Not used anymore
def SaveGraphHTML(user, exp, course):
    
    G = GenerateGraph(user, exp, course)
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

def GetGraphComponents(user, exp, course):
    
    G = GenerateGraph(user, exp, course)
    G = SetGraphProperties(G, exp)
    in_centrality = nx.in_degree_centrality(G)
    #print(G.edges(data=True))
    g=Network(height=800,width=800,notebook=False, directed=True)
    g.from_nx(G)
    
    nodes, edges, heading, height, width, options = g.get_network_data()
    node_info = {"in_centrality": in_centrality}
    return nodes, edges, node_info

def GetComparisonGraphComponents(comparison, exp):
    df = pd.read_csv('%s/%s.csv' % (comp_graph_dir, comparison), index_col=0)
    G = nx.from_pandas_adjacency(df, create_using=nx.DiGraph)
    G = SetGraphProperties(G, exp)
    in_centrality = nx.in_degree_centrality(G)
    #print(G.edges(data=True))
    g=Network(height=800,width=800,notebook=False, directed=True)
    g.from_nx(G)
    
    nodes, edges, heading, height, width, options = g.get_network_data()
    node_info = {"in_centrality": in_centrality}
    return nodes, edges, node_info

## Not used
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
Converts possible multiple user log files into a adjacency matrix

If the matrix already exists, then it adds the log file to that matrix.

Once the matrix is updated it will delete the log file
"""
def GenerateAdjacencyMatrix(user, exp, course, deleteLogFile = True):
    command_array, last_line = GetCommandList(user, exp, course)
   
    if(exp == "spinner"):
        nodes = ['voltage_step', 'voltage_ramp', 'position_step', 'position_ramp', 'speed_step', 'speed_ramp']
    elif(exp == "pendulum"):
        nodes = ['start','brake','load','free','sampling','drive_perc','brake_perc','measuring_tools']
    else:
        nodes = []

    # if an adjacency matrix for a user already exists, then add new data to that
    filename = '%s-%s-%s-adjacency.csv' % (user, exp, course)
    if(os.path.isfile('%s/%s' % (data_dir, filename))):
        df = pd.read_csv('%s/%s' % (data_dir, filename), index_col=0)
    else:
        matrix = np.zeros(shape=(len(nodes), len(nodes)))
        df = pd.DataFrame(matrix, nodes, nodes)

    ## add additional weight to the adjacency matrix
    ## this order of the rows and columns is necessary to get the correct direction on graphs when drawing a graph
    for index, command in enumerate(command_array):
        if(index + 1 < len(command_array)):
            df[command_array[index+1]][command] += 1

    # output the updated csv to file
    df.to_csv('%s/%s' % (data_dir, filename))

    # for storage reasons remove the log list json files
    # only do this if log files actually exist - ie the command array had at least one entry
    if(deleteLogFile and len(command_array) > 1):
        for file in glob.glob(data_dir + '/%s-*-%s-%s.json' % (user, exp, course)):
            os.remove(file)
        # need to maintain the latest command however to generate the correct edge for the next mode set
        # can this be changed to open with 'w' instead of removing file and then open 'a'?
        hardware = last_line["hardware"]
        with open('%s/%s-%s-%s-%s.json' % (data_dir, user, hardware, exp, course), 'w') as f:
            f.write(json.dumps(last_line))
            f.write('\n')

    return df

'''
Function for extracting timestamp info from a json message
'''
def getTimestampOfLog(log):
    return log['t']

"""
Generates a list of student commands from the user log files
Sorts all commands by timestamp
Returns an array of commands sent to hardware
Also returns the last line of the command list for storage
"""
def GetCommandList(user, exp, course):
    log_array = []
    command_array = []
    last_line = ''
    num_files = 0
    # go through individual log files associated with a user, course, exp to form a single array of json messages
    for file in glob.glob(data_dir + '/%s-*-%s-%s.json' % (user, exp, course)):
        num_files += 1
        with open(file) as f:
            lines = f.readlines()
            if len(lines) == 0:
                pass
            elif len(lines) == 1:
                try:
                    log = json.loads(lines[0])
                    log_array.append(log)
                except:
                    pass
            else:
                for index, line in enumerate(lines):
                    if len(line)>1:
                        try:
                            log = json.loads(line)
                            log_array.append(log)
                        except:
                            pass

    #sort that array by timestamp if there were multiple files, else the order will already be correct
    if(num_files > 1):
        log_array.sort(key=getTimestampOfLog)

    # loop through log_array to read out commands only into command_array
    
    for log_data in log_array:
        if len(log_data)>1:
            try:
                
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
                elif(log_data["payload"]["log"] == 'start'):
                    command_array.append('start')
                elif(log_data["payload"]["log"] == 'brake'):
                    command_array.append('brake')
                elif(log_data["payload"]["log"] == 'free'):
                    command_array.append('free')
                elif(log_data["payload"]["log"] == 'load'):
                    command_array.append('load')
                elif(log_data["payload"]["log"] == 'sampling'):
                    command_array.append('sampling')
                elif(log_data["payload"]["log"] == 'drive_perc'):
                    command_array.append('drive_perc')
                elif(log_data["payload"]["log"] == 'brake_perc'):
                    command_array.append('brake_perc')
                elif(log_data["payload"]["log"] == 'measuring_tools'):
                    command_array.append('measuring_tools')
                else:
                    pass

            except:
                pass
        ## the last message is whatever log_data is once it reaches here
        last_line = log_data
    
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

    elif(exp == 'pendulum'):
        x = {'start': -100, 'brake': 100, 'free': 200, 'load': 200, 'sampling': 100, 'drive_perc': -100, 'brake_perc': -200, 'measuring_tools': -200}
        y = {'start': 200, 'brake': 200, 'free': 100, 'load': -100, 'sampling': -200, 'drive_perc': -200, 'brake_perc': -100, 'measuring_tools': 100}
        nx.set_node_attributes(G, x, 'x')
        nx.set_node_attributes(G, y, 'y')

        #make sure physics doesn't shift the positions
        nx.set_node_attributes(G, False, name='physics')

        #ensure graph has labels of edge weights.
        edge_labels = dict([((u,v), str(int(d['weight']))) for u,v,d in G.edges(data=True)])
        nx.set_edge_attributes(G, edge_labels, name='label')

    return G


def GetUserFeedback(user_id, exp, course):
    filename = '%s-%s-%s-feedback.csv' % (user_id, exp, course)
    if(os.path.isfile('%s/%s' % (data_dir, filename))):
        df = pd.read_csv('%s/%s' % (data_dir, filename), index_col=0)
        exists = True
    else:
        df = pd.DataFrame()
        exists = False

    return df, exists


'''
Checks the number of logs in a student log file, if > n processes the log file into an adjacency matrix
'''
def AutoConvertLogs(mes, n, deleteLogFile = True):
    user = mes['user']
    exp = mes['exp']
    course = mes['course']
    hardware = mes["hardware"]

    filename = '%s-%s-%s-%s.json' % (user, hardware, exp, course)
    num_logs = 0

    with open('%s/%s' % (data_dir, filename), 'r') as log_file:
        num_logs = len(log_file.readlines())
    
    if(num_logs > n):
        GenerateAdjacencyMatrix(user, exp, course, deleteLogFile)
