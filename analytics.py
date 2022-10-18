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
Compares two graphs using the provided model for TaskDistance
Outputs a TaskDistance dissimilarity value
"""
def CompareTwoGraphs(user, comparison, a, b, p = 2, u = 2, l = -1):
    return


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