#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analytics.py

Methods for running analysis of student log files.

Compares student to comparison graphs, using TaskDistance models.

@author: dprydereid@gmail.com
"""
import pandas as pd
from TaskDistance import TaskDistance
import process
import os
from pathlib import Path


"""
Compares two graphs using the provided model for TaskDistance
Outputs a TaskDistance dissimilarity value

user (Dataframe): user adjacency matrix as a pandas Dataframe
comparison (Dataframe): the comparison adjacency matrix as a pandas Dataframe
a, b, p, u, l (float): the TaskDistance model to use to calculate distance
"""
def DistanceBetweenGraphs(user, comparison, a, b, p = 2, u = 2, l = -1):

    distance = TaskDistance(user, comparison, a, b, p, u, l)

    return distance


"""
Returns TaskDistance to each comparison model.

user (Dataframe): user adjacency matrix as a pandas Dataframe
exp (string): name of the experiment

"""
def TaskIdentification(user, exp, a = 10, b = 1, p = 2, u = 2, l = -1):
    td = {}
    for file in os.listdir('./comparison_graphs'):
        if file.startswith(exp):
            task_name = Path(file).stem
            comp = pd.read_csv('./comparison_graphs/%s' % file, index_col=0)
            task_dist = DistanceBetweenGraphs(user, comp, a, b, p, u, l)
            td[task_name] = task_dist
    
    return td


"""
Returns a value for student exploration of hardware space, based on the exploration model of TaskDistance

user (Dataframe): user adjacency matrix as a pandas Dataframe
exp (string): name of the experiment
"""
def Exploration(user, exp, a = 0, b = 10, p = 2, u = 2, l = -1):
    comp = pd.read_csv('./comparison_graphs/%s-all.csv' % exp, index_col=0)
    task_dist = DistanceBetweenGraphs(user, comp, a, b, p, u, l)
    
    return task_dist

"""
Returns a value for centroid of student graph and centroids for specific tasks

user (Dataframe): user adjacency matrix as a pandas Dataframe
exp (string): name of the experiment
"""
def Centroid(user, exp):
    print(user)
    if(exp == 'spinner'):
        return {"student": [0.5,0.5], "task1": [1,1], "task3": [0,0], "task4": [-1,0]}
    else:
        return {"student": [0,0], "task1": [0,0], "task3": [0,0], "task4": [0,0]} 