#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
## Uses the graph-comparison.csv file to evaluate which task a user completed.
## OUPUT: csv file of user and task

import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description='Read .csv file of graph_comparisons.')
parser.add_argument('--file', dest='file', type=str, help='the file containing graph comparison data')
parser.add_argument('--distance', dest='distance', type=str, help='the distance measure to use for task identification')

args = parser.parse_args()
file = args.file
dist_measure = args.distance

df = pd.read_csv(file, index_col=0)

usernames = df['graph1'].unique()       #get all usernames

output = []

for username in usernames:
    df_user = df.query("graph1 == @username")
    min_value = df_user[dist_measure].min()

    df_min = df_user[df_user[dist_measure] == min_value]
    
    if(len(df_min) > 0):
        data = {'User': username, 'Min Tasks': list(df_min['graph2']), 'distance': df_min[dist_measure].values[0]}
    else:
        data = {'User': username, 'Min Tasks': 'Empty Graph', 'distance': 'NA'}
    
    output.append(data)

df_out = pd.DataFrame(data=output)
path = os.path.dirname(file)

if(dist_measure == 'taskdistance'):
    df_out.to_csv('%s/graph-minima.csv' % path, mode='w', header=True)
else:
    df_out.to_csv('%s/graph-minima-%s.csv' % (path, dist_measure), mode='w', header=True)
##========================
## Count task completion

tasks = {'h': 'empty', 
        'expert-task-total-graph-adjacency': 'total', 
        'expert-task1-2-graph-adjacency': '1-2',
        'expert-task3-graph-adjacency': '3',
        'expert-task4-graph-adjacency': '4',
        'expert-task1-2-3-graph-adjacency': '1-2-3',
        'expert-task1-2-4-graph-adjacency': '1-2-4',
        'expert-task3-4-graph-adjacency': '3-4'}
df_out['task'] = df_out['Min Tasks'].str[-1]

df_out['task'] = df_out['task'].map(tasks)
if(dist_measure == 'taskdistance'):
    df_out['task'].value_counts().to_csv('%s/task-counts.csv' % path, mode='w', header=True)
else:
    df_out['task'].value_counts().to_csv('%s/task-counts-%s.csv' % (path, dist_measure), mode='w', header=True)