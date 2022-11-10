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
import math

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
Returns a value for student enjoyment of the lab as a sum of positive and negative responses to the lab

user (Dataframe): user adjacency matrix as a pandas Dataframe
exp (string): name of the experiment
"""
def Enjoyment(user_id, exp):
    feedback, exists = process.GetUserFeedback(user_id, exp)
    ## get sum of positive responses
    positive = 0
    negative = 0
    if(exists):
        positive += feedback.loc['Engaged'].sum()
        positive += feedback.loc['Curious'].sum()
        positive += feedback.loc['Interested'].sum()
        positive += feedback.loc['Excited'].sum()
        positive += feedback.loc['Satisfied'].sum()
        ## get sum of negative responses
        negative += feedback.loc['Dissatisfied'].sum()
        negative += feedback.loc['Bored'].sum()
        negative += feedback.loc['Confused'].sum()
        negative += feedback.loc['Uninterested'].sum()
        negative += feedback.loc['Frustrated'].sum()

    return positive-negative
    
    
    


"""Takes an adjacency matrix representation of a graph and the index of the node we want to calculate mass for.

        Parameters:
        A (adjacency matrix): A Pandas Dataframe representation of the adjacency matrix of a graph
        node (string): the string name of the node that we want the "mass" of. 

        Returns:
        m (int): the effective mass of that node
"""
def NodeEffectiveMass(A, node):
    mass = A[node].sum()
    return mass


"""Returns the centroid of a graph. Equivalent to the centre of mass of a set of particles, with graph nodes representing 
particles with equivalent mass equal to the sum of edge weights that are incident on that node.

        Parameters:
        A (Pandas Dataframe): The adjacency matrix for the graph, with column and row indices with the names of the nodes
        node_positions (list): a list of node positions [{'name':'voltage_step', 'x':1,'y':-1} ...]

        Returns:
        float[]: (x,y) the centroid as a point in the projected graph space. 
"""
def graphCentroid(A, node_positions):
    M = 0
    R_x = 0
    R_y = 0

    for node in node_positions:
        name = node['name']
        x = node['x']
        y = node['y']
        m = NodeEffectiveMass(A, name)
        M += m
        R_x += m*x
        R_y += m*y
    
    if(M > 0):
        return [R_x/M, R_y/M]
    else:
        return [float('nan'), float('nan')]

"""
Returns a value for centroid of student graph and centroids for specific tasks

user (Dataframe): user adjacency matrix as a pandas Dataframe
exp (string): name of the experiment
"""
def Centroid(user, exp):
    
    if(exp == 'spinner'):
        vertex_positions = [{'name':'voltage_step', 'x':0.5,'y':math.sin(math.pi/3)}, 
                            {'name':'voltage_ramp', 'x':-0.5,'y':math.sin(math.pi/3)}, 
                            {'name':'position_step', 'x':1,'y':0}, 
                            {'name':'position_ramp', 'x':-1,'y':0}, 
                            {'name':'speed_step', 'x':0.5,'y':-math.sin(math.pi/3)}, 
                            {'name':'speed_ramp', 'x':-0.5,'y':-math.sin(math.pi/3)}]

        student = graphCentroid(user, vertex_positions)
        task1 = graphCentroid(pd.read_csv('./comparison_graphs/spinner-1-2.csv', index_col=0), vertex_positions)
        task3 = graphCentroid(pd.read_csv('./comparison_graphs/spinner-3.csv', index_col=0), vertex_positions)
        task4 = graphCentroid(pd.read_csv('./comparison_graphs/spinner-4.csv', index_col=0), vertex_positions)
        all = graphCentroid(pd.read_csv('./comparison_graphs/spinner-all.csv', index_col=0), vertex_positions)

        return {"student": student, "task1": task1, "task3": task3, "task4": task4, "all": all, "vertices": vertex_positions}

    else:

        return {"student": [0,0], "task1": [0,0], "task3": [0,0], "task4": [0,0], "all": [0,0]} 