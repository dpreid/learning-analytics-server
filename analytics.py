#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analytics.py

Methods for running analysis of student log files.

Compares student to comparison graphs, using TaskDistance models.

@author: dprydereid@gmail.com
"""
import pandas as pd
from TaskDistance import TaskDistance, checkMissingEdge
import process
import os
from pathlib import Path
import math

comp_graph_dir = os.environ.get("COMP_PATH", "./comparison_graphs")

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
def TaskIdentification(user, exp, course, a = 10, b = 1, p = 2, u = 2, l = -1):
    td = {}
    filestart = '%s-%s' % (exp, course)
    for file in os.listdir(comp_graph_dir):
        if file.startswith(filestart):
            task_name = Path(file).stem
            comp = pd.read_csv('%s/%s' % (comp_graph_dir, file), index_col=0)
            task_dist = DistanceBetweenGraphs(user, comp, a, b, p, u, l)
            td[task_name] = task_dist
    
    return td

"""
Returns comments that compare a student graph to a given task comparison graph.

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
compare_task (string): name of the comparison task

"""
def TaskFeedback(user_A, compare_task):
    task_feedback = {'hardware': [], 'hardware_freq': [], 'transition': [], 'transition_freq': []}
    B = pd.read_csv('%s/%s.csv' % (comp_graph_dir, compare_task), index_col=0)
    rows = user_A.shape[0]
    cols = user_A.shape[1]
    for i in range(0, rows):
            for j in range(0, cols):
                if(checkMissingEdge(user_A.iloc[i,j], B.iloc[i,j])):
                    if(i == j):
                        task_feedback['hardware'].append(user_A.columns.values[j])
                    else:
                        task_feedback['transition'].append(user_A.index.values[i] + ' to ' + user_A.columns.values[j])

                elif(user_A.iloc[i,j] - B.iloc[i,j] < 0):
                    if(i == j):
                        task_feedback['hardware_freq'].append(user_A.columns.values[j])
                    else:
                        task_feedback['transition_freq'].append(user_A.index.values[i] + ' to ' + user_A.columns.values[j])

    return task_feedback

"""
Returns a value for student exploration of hardware space, based on the exploration model of TaskDistance

user (Dataframe): user adjacency matrix as a pandas Dataframe
exp (string): name of the experiment
"""
def Exploration(user, exp, course, a = 0, b = 10, p = 2, u = 2, l = -1):
    try:
        comp = pd.read_csv('%s/%s-%s-all.csv' % (comp_graph_dir, exp, course), index_col=0)
        task_dist = DistanceBetweenGraphs(user, comp, a, b, p, u, l)

        return task_dist
    except:
        print('no full task to compare to')
        return 0
    

"""
Returns a value for student enjoyment of the lab as a sum of positive and negative responses to the lab

user (Dataframe): user adjacency matrix as a pandas Dataframe
exp (string): name of the experiment
"""
def Enjoyment(user_id, exp, course):
    feedback, exists = process.GetUserFeedback(user_id, exp, course)
    ## get sum of positive responses
    positive = 0
    negative = 0
    if(exists):
        positive += feedback.loc['Engaged'].sum()
        positive += feedback.loc['Curious'].sum()
        positive += feedback.loc['Delighted'].sum()
        ## get sum of negative responses
        negative += feedback.loc['Bored'].sum()
        negative += feedback.loc['Confused'].sum()
        negative += feedback.loc['Frustrated'].sum()
        negative += feedback.loc['Surprised'].sum()
        negative += feedback.loc['Anxious'].sum()

    return positive-negative
    
"""
Returns the percentage of edges in the student graph in comparison to the expected full procedure

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
exp (string): name of the experiment
course (string): the course the student is enrolled on
"""
def TotalEdges(user_A, exp, course):
    if(exp == 'spinner' and course == 'cie3'):
        expected_graph = pd.read_csv('%s/spinner-cie3-all.csv' % comp_graph_dir, index_col=0)
    elif(exp == 'spinner' and course == 'engdes1'):
        expected_graph = pd.read_csv('%s/spinner-engdes1-all.csv' % comp_graph_dir, index_col=0)
    elif(exp == 'pendulum' and course == 'engdes1'):
        expected_graph = pd.read_csv('%s/pendulum-engdes1-all.csv' % comp_graph_dir, index_col=0)

    expected_total = expected_graph.to_numpy().sum()
    student_total = user_A.to_numpy().sum()

    return student_total * 100.0 / expected_total
    


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
def Centroid(user, exp, course):
    
    if(exp == 'spinner' and course == 'cie3'):
        vertex_positions = [{'name':'voltage_step', 'x':0.5,'y':math.sin(math.pi/3)}, 
                            {'name':'voltage_ramp', 'x':-0.5,'y':math.sin(math.pi/3)}, 
                            {'name':'position_step', 'x':1,'y':0}, 
                            {'name':'position_ramp', 'x':-1,'y':0}, 
                            {'name':'speed_step', 'x':0.5,'y':-math.sin(math.pi/3)}, 
                            {'name':'speed_ramp', 'x':-0.5,'y':-math.sin(math.pi/3)}]

        student = graphCentroid(user, vertex_positions)
        task1 = graphCentroid(pd.read_csv('%s/spinner-cie3-1-2.csv' % comp_graph_dir, index_col=0), vertex_positions)
        task3 = graphCentroid(pd.read_csv('%s/spinner-cie3-3.csv' % comp_graph_dir, index_col=0), vertex_positions)
        task4 = graphCentroid(pd.read_csv('%s/spinner-cie3-4.csv' % comp_graph_dir, index_col=0), vertex_positions)
        all = graphCentroid(pd.read_csv('%s/spinner-cie3-all.csv' % comp_graph_dir, index_col=0), vertex_positions)

        return {"student": student, "task1": task1, "task3": task3, "task4": task4, "all": all, "vertices": vertex_positions}
    
    elif(exp == 'spinner' and course == 'engdes1'):
        vertex_positions = [{'name':'voltage_step', 'x':0.5,'y':math.sin(math.pi/3)}, 
                            {'name':'voltage_ramp', 'x':-0.5,'y':math.sin(math.pi/3)}, 
                            {'name':'position_step', 'x':1,'y':0}, 
                            {'name':'position_ramp', 'x':-1,'y':0}, 
                            {'name':'speed_step', 'x':0.5,'y':-math.sin(math.pi/3)}, 
                            {'name':'speed_ramp', 'x':-0.5,'y':-math.sin(math.pi/3)}]

        student = graphCentroid(user, vertex_positions)
        task1core = graphCentroid(pd.read_csv('%s/spinner-engdes1-1-core.csv' % comp_graph_dir, index_col=0), vertex_positions)
        task1ext = graphCentroid(pd.read_csv('%s/spinner-engdes1-1-ext.csv' % comp_graph_dir, index_col=0), vertex_positions)
        task2 = graphCentroid(pd.read_csv('%s/spinner-engdes1-2.csv' % comp_graph_dir, index_col=0), vertex_positions)
        all = graphCentroid(pd.read_csv('%s/spinner-engdes1-all.csv' % comp_graph_dir, index_col=0), vertex_positions)

        return {"student": student, "task1core": task1core, "task1ext": task1ext, "task2": task2, "all": all, "vertices": vertex_positions}
    
    elif(exp == 'pendulum' and course == 'engdes1'):
        vertex_positions = [{'name':'start', 'x':0,'y':1},
                            {'name':'brake', 'x':0.64,'y':0.77}, 
                            {'name':'free', 'x':0.98,'y':0.17}, 
                            {'name':'load', 'x':0.87,'y':-0.5}, 
                            {'name':'sampling', 'x':0.34,'y':-0.94}, 
                            {'name':'drive_perc', 'x':-0.34,'y':-0.94}, 
                            {'name':'brake_perc', 'x':-0.87,'y':-0.5},
                            {'name':'measuring_tools', 'x':-0.98,'y':0.17},
                            {'name':'record', 'x':-0.64,'y':0.77}
                            ]

        student = graphCentroid(user, vertex_positions)
        task1core = graphCentroid(pd.read_csv('%s/pendulum-engdes1-1-core.csv' % comp_graph_dir, index_col=0), vertex_positions)
        task1ext = graphCentroid(pd.read_csv('%s/pendulum-engdes1-1-ext.csv' % comp_graph_dir, index_col=0), vertex_positions)
        task2 = graphCentroid(pd.read_csv('%s/pendulum-engdes1-2.csv' % comp_graph_dir, index_col=0), vertex_positions)
        all = graphCentroid(pd.read_csv('%s/pendulum-engdes1-all.csv' % comp_graph_dir, index_col=0), vertex_positions)

        return {"student": student, "task1core": task1core, "task1ext": task1ext, "task2": task2, "all": all, "vertices": vertex_positions}

    else:

        return {"student": [0,0], "task1": [0,0], "task3": [0,0], "task4": [0,0], "all": [0,0]} 