#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
## Uses the graph-comparison.csv file to evaluate which users have explored the physical hardware possibilities.
## OUPUT: csv file of user and distance to expert model

import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description='Read .csv file of graph_comparisons.')
parser.add_argument('--file', dest='file', type=str, help='the file containing graph comparison data')
parser.add_argument('--distance', dest='distance', type=str, help='the distance measure to use for exploration identification')

args = parser.parse_args()
file = args.file
dist_measure = args.distance

df = pd.read_csv(file, index_col=0)

usernames = df['graph1'].unique()       #get all usernames

output = []

for username in usernames:
    df_user = df.query("graph1 == @username")

    df_expert = df_user[df_user["graph2"] == "expert-task-total-graph-adjacency"]
    
    if(len(df_expert) > 0):
        data = {'User': username, 'Task': "expert-task-total-graph-adjacency", 'distance': df_expert[dist_measure].values[0]}
    else:
        data = {'User': username, 'Tasks': 'Empty Graph', 'distance': 'NA'}
    
    output.append(data)

df_out = pd.DataFrame(data=output)
path = os.path.dirname(file)

if(dist_measure == 'taskdistance_exploration'):
    df_out.to_csv('%s/graph-exploration.csv' % path, mode='w', header=True)
else:
    df_out.to_csv('%s/graph-exploration-%s.csv' % (path, dist_measure), mode='w', header=True)
