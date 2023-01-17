import unittest
import pandas as pd
import numpy as np
import process
import analytics
import os


class TestAnalytics(unittest.TestCase):

    def setUp(self):
        self.A = process.GenerateAdjacencyMatrix('test', 'exp', 'course', False)

    def tearDown(self):
        try:
            os.remove('./test/data/test-exp-course-adjacency.csv')
        except:
            pass
    
    def test_compare_arrays(self):
        ad1 = [[1,0,1,0,0,0],[0,0,0,0,0,0],[0,0,2,1,0,0],[0,0,1,3,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        ad2 = [[1,1,1,0,0,0],[0,0,0,0,0,0],[1,0,2,1,0,0],[0,0,1,3,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        ad1_pd = pd.DataFrame(data=ad1)
        ad2_pd = pd.DataFrame(data=ad2)
        distance = analytics.DistanceBetweenGraphs(ad1_pd, ad2_pd, 10, 1)
        self.assertEqual(distance, 20)
    @unittest.skip
    def test_distance_zero(self):
        distance = analytics.DistanceBetweenGraphs(self.A, self.A, 10, 1)
        self.assertEqual(distance, 0)
    @unittest.skip
    def test_distance_zero2(self):
        compare = pd.read_csv('./test/data/spinner-compare-same.csv', index_col=0)
        distance = analytics.DistanceBetweenGraphs(compare, compare, 10, 1)
        self.assertEqual(distance, 0)
    @unittest.skip
    def test_distance_zero3(self):
        compare = pd.read_csv('./test/data/spinner-compare-same.csv', index_col=0)
        distance = analytics.DistanceBetweenGraphs(self.A, compare, 10, 1)
        self.assertEqual(distance, 0)
    @unittest.skip
    def test_distance_missing(self):
        compare = pd.read_csv('./test/data/spinner-compare-1.csv', index_col=0)
        distance = analytics.DistanceBetweenGraphs(self.A, compare, 10, 1)
        self.assertEqual(distance, 20)
    @unittest.skip
    def test_distance_extra(self):
        compare = pd.read_csv('./test/data/spinner-compare-2.csv', index_col=0)
        distance = analytics.DistanceBetweenGraphs(self.A, compare, 10, 1)
        self.assertEqual(distance, 3)
    @unittest.skip
    def test_feedback_0_content(self):
        feedback = analytics.TaskFeedback(self.A, 'spinner-cie3-1-2')
        with self.subTest():
            self.assertEqual(['voltage_step'], feedback['hardware_freq'])
        with self.subTest():
            self.assertEqual([], feedback['hardware'])
        with self.subTest():
            self.assertEqual([], feedback['transition'])
        with self.subTest():
            self.assertEqual([], feedback['transition_freq'])
    @unittest.skip
    def test_feedback_1_content(self):
        feedback = analytics.TaskFeedback(self.A, 'spinner-cie3-1-2-3')
        with self.subTest():
            self.assertEqual(['voltage_step'], feedback['hardware_freq'])
        with self.subTest():
            self.assertEqual([], feedback['hardware'])
        with self.subTest():
            self.assertEqual([], feedback['transition'])
        with self.subTest():
            self.assertEqual([], feedback['transition_freq'])
    @unittest.skip
    def test_feedback_2_content(self):
        feedback = analytics.TaskFeedback(self.A, 'spinner-cie3-all')
        with self.subTest():
            self.assertEqual(['voltage_step', 'position_step'], feedback['hardware_freq'])
        with self.subTest():
            self.assertEqual([], feedback['hardware'])
        with self.subTest():
            self.assertEqual([], feedback['transition'])
        with self.subTest():
            self.assertEqual([], feedback['transition_freq'])

    @unittest.skip
    def test_feedback_3_content(self):
        A = pd.read_csv('./test/data/spinner-compare-4.csv', index_col=0)
        feedback = analytics.TaskFeedback(A, 'spinner-cie3-3')
        with self.subTest():
            self.assertEqual(['position_step', 'position_ramp'], feedback['hardware'])
        with self.subTest():
            self.assertEqual(['position_step to position_ramp'], feedback['transition'])
        with self.subTest():
            self.assertEqual([], feedback['hardware_freq'])
        with self.subTest():
            self.assertEqual([], feedback['transition_freq'])

    @unittest.skip
    def test_total_edges_0(self):
        total = analytics.TotalEdges(self.A, 'spinner', 'cie3')
        self.assertEqual(total, 900/439)
    @unittest.skip
    def test_total_edges_1(self):
        compare = pd.read_csv('./comparison_graphs/spinner-cie3-1-2.csv', index_col=0)
        total = analytics.TotalEdges(compare, 'spinner', 'cie3')
        self.assertEqual(total, 40300/439)

    


if __name__ == '__main__':
    unittest.main()