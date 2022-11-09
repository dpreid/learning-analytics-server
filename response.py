#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analytics.py

Methods for running analysis of student log files.

Compares student to comparison graphs, using TaskDistance models.

@author: dprydereid@gmail.com
"""
import pandas as pd
import process
import analytics


"""
Generates the JSON analytics response to send back to a user

user (Dataframe): user adjacency matrix as a pandas Dataframe

"""
def TestResponse(user_A, user_id, exp):
    taskdistance_all = analytics.DistanceBetweenGraphs(user_A, pd.read_csv('./comparison_graphs/%s-all.csv' % exp, index_col=0), 10, 1)
    nodes, edges = process.GetGraphComponents(user_id, exp)
    response = {"user": user_id, "type":"response", "exp": exp, "nodes": nodes, "edges": edges, "taskdistance": taskdistance_all}

    return response


"""
Generates the JSON response to send back to a user for a graph request

user_id (string): user UUID
exp (string): the remote lab hardware

"""
def StudentGraphResponse(user_id, exp):
    nodes, edges = process.GetGraphComponents(user_id, exp)
    response = {"user": user_id, "type":"response", "exp": exp, "content":"student_graph", "nodes": nodes, "edges": edges}

    return response

"""
Generates the JSON response to send back to a user for a comparison graph request

comparison (string): the comparison task model to return
exp (string): the remote lab hardware

"""
def ComparisonGraphResponse(comparison, user_id, exp):
    nodes, edges = process.GetComparisonGraphComponents(comparison, exp)
    response = {"user": user_id, "type":"response", "exp": exp, "content":"comparison_graph", "nodes": nodes, "edges": edges}

    return response

"""
Generates the JSON response to send back to a user for a task completion request

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
user_id (string): user UUID
exp (string): the remote lab hardware

"""
def TaskCompletionResponse(user_A, user_id, exp):
    task_dists = analytics.TaskIdentification(user_A, exp)
    response = {"user": user_id, "type":"response", "exp": exp, "content":"task_identification", "tasks": task_dists}

    return response

"""
Generates the JSON response to send back to a user for an exploration request

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
user_id (string): user UUID
exp (string): the remote lab hardware

"""
def IndicatorResponse(user_A, user_id, exp):
    exploration = analytics.Exploration(user_A, exp)
    response = {"user": user_id, "type":"response", "exp": exp, "content":"indicators", "indicators": {"exploration": exploration}}

    return response

"""
Generates the JSON response to send back to a user for a centroid request

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
user_id (string): user UUID
exp (string): the remote lab hardware

"""
def CentroidResponse(user_A, user_id, exp):
    centroids = analytics.Centroid(user_A, exp)
    response = {"user": user_id, "type":"response", "exp": exp, "content":"centroids", "centroids": centroids}

    return response

