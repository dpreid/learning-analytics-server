import unittest
import pandas as pd
import numpy as np
import process
import analytics
import os


class TestAnalytics(unittest.TestCase):

    def setUp(self):
        self.A = process.GenerateAdjacencyMatrix('analytics', 'spinner', False)

    def tearDown(self):
        try:
            os.remove('./test/data/analytics-spinner-adjacency.csv')
        except:
            pass

    def test_compare_arrays(self):
        ad1 = [[1,0,1,0,0,0],[0,0,0,0,0,0],[0,0,2,1,0,0],[0,0,1,3,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        ad2 = [[1,1,1,0,0,0],[0,0,0,0,0,0],[1,0,2,1,0,0],[0,0,1,3,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        ad1_pd = pd.DataFrame(data=ad1)
        ad2_pd = pd.DataFrame(data=ad2)
        distance = analytics.DistanceBetweenGraphs(ad1_pd, ad2_pd, 10, 1)
        self.assertEqual(distance, 20)

    def test_distance_zero(self):
        distance = analytics.DistanceBetweenGraphs(self.A, self.A, 10, 1)
        self.assertEqual(distance, 0)

    def test_distance_zero2(self):
        compare = pd.read_csv('./test/data/spinner-compare-same.csv', index_col=0)
        distance = analytics.DistanceBetweenGraphs(compare, compare, 10, 1)
        self.assertEqual(distance, 0)

    def test_distance_zero3(self):
        compare = pd.read_csv('./test/data/spinner-compare-same.csv', index_col=0)
        distance = analytics.DistanceBetweenGraphs(self.A, compare, 10, 1)
        self.assertEqual(distance, 0)

    def test_distance_missing(self):
        compare = pd.read_csv('./test/data/spinner-compare-1.csv', index_col=0)
        distance = analytics.DistanceBetweenGraphs(self.A, compare, 10, 1)
        self.assertEqual(distance, 20)

    def test_distance_extra(self):
        compare = pd.read_csv('./test/data/spinner-compare-2.csv', index_col=0)
        distance = analytics.DistanceBetweenGraphs(self.A, compare, 10, 1)
        self.assertEqual(distance, 3)



    


if __name__ == '__main__':
    unittest.main()