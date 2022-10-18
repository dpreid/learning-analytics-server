#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
## Package including custom distance measures for graphs of hardware state from remote lab learning analytics.

from cmath import nan
import numpy as np


def checkMissingEdge(Aij, Bij):
    if(Aij == 0 and Bij != 0):
        return True
    else:
        return False

def checkAdditionalEdge(Aij, Bij):
    if(Aij != 0 and Bij == 0):
        return True
    else:
        return False

"""Returns the distance factor depending on the weight difference between two edges - includes a quadratic factor. 

        Parameters:
        Aij (array): Edge Aij weight
        B (array): Edge Bij weight
        a (float): the distance factor for missing edges
        b (float): the distance factor for additional edges
        upperMax(float): how many times larger A needs to be over B for it to hit the limit
        lowerMax(float): how many times smaller A needs to be over B for it to hit the limit

        Returns:
        float: distance
"""
def checkDifferenceWeightQuadratic(Aij, Bij, a, b, upperMax, lowerMax):
    norm_diff = (Aij - Bij) / Bij

    if(norm_diff >= 0 and norm_diff <= upperMax):
        return b*(norm_diff*norm_diff)/(upperMax*upperMax)
    elif(norm_diff > upperMax):
        return b
    elif(norm_diff < 0 and norm_diff >= lowerMax):
        return a*norm_diff*norm_diff
    else:
        return a

"""Returns the distance factor depending on the weight difference between two edges - linear in normalised weight difference up to a cutoff

        Parameters:
        Aij (array): Edge Aij weight
        B (array): Edge Bij weight
        a (float): the distance factor for missing edges
        b (float): the distance factor for additional edges
        upperMax(float): how many times larger A needs to be over B for it to hit the limit
        lowerMax(float): how many times smaller A needs to be over B for it to hit the limit

        Returns:
        float: distance
"""
def checkDifferenceWeight(Aij, Bij, a, b, upperMax, lowerMax):
    norm_diff = (Aij - Bij) / Bij

    if(norm_diff >= 0 and norm_diff <= upperMax):
        return b*norm_diff/upperMax
    elif(norm_diff > upperMax):
        return b
    elif(norm_diff < 0 and norm_diff >= lowerMax):
        return a*np.abs(norm_diff)/np.abs(lowerMax)
    else:
        return a


"""Returns the Task Distance (TD) between two adjacency matrices. Returns a dissimilarity value > 0, not a similarity.

        Parameters:
        A (array): An adjacency matrix as an array, the student task graph
        B (array): An adjacency matrix as an array, the expert graph to compare to
        a (float): the distance factor for missing edges
        b (float): the distance factor for additional edges
        loopFactor (float): how many times greater a self-loop impacts distance than a regular node to node edge.
        upperMax (float): cutoff for larger weighted edges to stop contributing to distance
        lowerMax (float): cutoff for smaller weighted edges to stop contributing to distance

        Returns:
        float: ITD distance
"""
def TaskDistance(A, B, a, b, loopFactor = 2, upperMax = 2, lowerMax = -1):
    D = 0
    diff_weight = 0
    diff_weight_count = 0
    rows = A.shape[0]
    cols = A.shape[1]
    ## Check for an empty graph - this should return NaN
    if(A.sum().sum() == 0):
        D = float('nan')
    else:
    ##else calculate distance
        for i in range(0, rows):
            for j in range(0, cols):
                if(checkMissingEdge(A.iloc[i,j], B.iloc[i,j])):
                    ## self-loop weighted more
                    if(i==j):
                        D += loopFactor*a
                    else:
                        D += a
                elif(checkAdditionalEdge(A.iloc[i,j], B.iloc[i,j])):
                    ## self-loop weighted more
                    if(i==j):
                        D += loopFactor*b
                    else:
                        D += b
                else:
                    if(A.iloc[i,j] == B.iloc[i,j]):
                        pass
                    else:
                        diff_weight_count += 1
                        diff_weight += checkDifferenceWeight(A.iloc[i,j], B.iloc[i,j], a, b, upperMax, lowerMax)

        if(diff_weight_count > 0):
            diff_weight_norm = diff_weight/diff_weight_count
            D += diff_weight_norm

    return D