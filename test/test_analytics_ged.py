import unittest
import pandas as pd
import numpy as np
import process
import analytics
import os


class TestAnalytics(unittest.TestCase):

    
    def test_distance_ged_1(self):
        user = [[1,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        comparison = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        user_df = pd.DataFrame(data=user)
        comparison_df = pd.DataFrame(data=comparison)
        distance = analytics.DistanceBetweenGraphs(user_df, comparison_df, algorithm="ged")
        self.assertEqual(distance, 1)

    def test_distance_ged_2(self):
        user = [[1,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        comparison = [[0,1,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        user_df = pd.DataFrame(data=user)
        comparison_df = pd.DataFrame(data=comparison)
        distance = analytics.DistanceBetweenGraphs(user_df, comparison_df, algorithm="ged")
        self.assertEqual(distance, 2)

    def test_distance_ged_3(self):
        user = [[10,0,4,0,0,0],[5,0,0,0,0,0],[0,0,0,6,0,0],[0,0,0,0,0,0],[0,0,20,0,0,0],[0,0,0,0,0,0]]
        comparison = [[5,1,0,0,0,0],[4,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,21,0,0,0],[0,0,0,0,0,0]]
        user_df = pd.DataFrame(data=user)
        comparison_df = pd.DataFrame(data=comparison)
        distance = analytics.DistanceBetweenGraphs(user_df, comparison_df, algorithm="ged")
        self.assertEqual(distance, 18)
    
    

    


if __name__ == '__main__':
    unittest.main()