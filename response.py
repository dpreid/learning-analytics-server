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
import os

comp_graph_dir = os.environ.get("COMP_PATH", "./comparison_graphs")

"""
Generates the JSON analytics response to send back to a user

user (Dataframe): user adjacency matrix as a pandas Dataframe

"""
def TestResponse(user_A, user_id, exp):
    taskdistance_all = analytics.DistanceBetweenGraphs(user_A, pd.read_csv('%s/%s-all.csv' % (comp_graph_dir, exp), index_col=0), 10, 1)
    nodes, edges = process.GetGraphComponents(user_id, exp)
    response = {"user": user_id, "type":"response", "exp": exp, "nodes": nodes, "edges": edges, "taskdistance": taskdistance_all}

    return response


"""
Generates the JSON response to send back to a user for a graph request

user_id (string): user UUID
exp (string): the remote lab hardware

"""
def StudentGraphResponse(user_id, exp, course):
    nodes, edges, node_info = process.GetGraphComponents(user_id, exp, course)
    
    response = {"user": user_id, "type":"response", "exp": exp, "course": course, "content":"student_graph", "nodes": nodes, "edges": edges, "node_info": node_info}

    return response

"""
Generates the JSON response to send back to a user for a comparison graph request

comparison (string): the comparison task model to return
exp (string): the remote lab hardware

"""
def ComparisonGraphResponse(comparison, user_id, exp):
    nodes, edges, node_info = process.GetComparisonGraphComponents(comparison, exp)
    response = {"user": user_id, "type":"response", "exp": exp, "content":"comparison_graph", "nodes": nodes, "edges": edges, "node_info": node_info}

    return response

"""
Generates the JSON response to send back to a user for a task completion request

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
user_id (string): user UUID
exp (string): the remote lab hardware

"""
def TaskCompletionResponse(user_A, user_id, exp, course, algorithm = 'taskcompare'):
    if(exp == 'spinner'):
        task_dists = analytics.TaskIdentification(user_A, exp, course, algorithm)
    elif(exp == 'pendulum'):
        task_dists = analytics.TaskIdentification(user_A, exp, course, algorithm)
    response = {"user": user_id, "type":"response", "exp": exp, "course": course, "content":"task_identification", "tasks": task_dists}

    return response


"""
Generates the JSON response to send back to a user for a task compare request

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
user_id (string): user UUID
compare_task (string): the comparison model to compare to
exp (string): the remote lab hardware
course (string): the course that a student is enrolled in

"""
def TaskFeedbackResponse(user_A, user_id, compare_task, exp, course):
    task_feedback = analytics.TaskFeedback(user_A, compare_task)
    response = {"user": user_id, "type":"response", "exp": exp, "course": course, "content":"task_feedback", "feedback": task_feedback}

    return response

"""
Generates the JSON response to send back to a user for an exploration request

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
user_id (string): user UUID
exp (string): the remote lab hardware

"""
def IndicatorResponse(user_A, user_id, exp, course):
    exploration = analytics.Exploration(user_A, exp, course)
    enjoyment = analytics.Enjoyment(user_id, exp, course)
    total = analytics.TotalEdges(user_A, exp, course)
    response = {"user": user_id, "type":"response", "exp": exp, "course": course, "content":"indicators", "indicators": {"exploration": exploration, "enjoyment": enjoyment, "edges": total}}

    return response

"""
Generates the JSON response to send back to a user for a centroid request

user_A (Dataframe): user adjacency matrix as a pandas Dataframe
user_id (string): user UUID
exp (string): the remote lab hardware

"""
def CentroidResponse(user_A, user_id, exp, course):
    centroids = analytics.Centroid(user_A, exp, course)
    response = {"user": user_id, "type":"response", "exp": exp, "course": course, "content":"centroids", "centroids": centroids}

    return response

