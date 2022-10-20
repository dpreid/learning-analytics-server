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


"""
Generates the JSON analytics response to send back to a user

user (Dataframe): user adjacency matrix as a pandas Dataframe

"""
def AnalyticsResponse(user, exp):
    taskdistance_all = DistanceBetweenGraphs(user, pd.read_csv('/comparison_graphs/%s-all.csv' % exp, index_col=0), 10, 1)

    return {"type":"response", "taskdistance": taskdistance_all}

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
Identifies the closest comparison graph with the specified model of TaskDistance
Returns that closest graph name
"""
def TaskIdentification(user, comparison, a = 10, b = 1, p = 2, u = 2, l = -1):
    return


"""
Returns a value for student exploration of hardware space, based on the exploration model of TaskDistance
"""
def Exploration(user, comparison, a = 0, b = 10, p = 2, u = 2, l = -1):
    return