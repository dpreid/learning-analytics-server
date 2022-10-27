import unittest
import pandas as pd
import numpy as np
import process
import analytics
import os


class TestResponse(unittest.TestCase):

    def setUp(self):
        self.A = process.GenerateAdjacencyMatrix('analytics', 'spinner', False)

    def tearDown(self):
        try:
            os.remove('./test/data/analytics-spinner-adjacency.csv')
        except:
            pass

    def test_taskidentification(self):
        td = analytics.TaskIdentification(self.A, 'spinner')
        with self.subTest():
            self.assertIn('spinner-3', td)
        with self.subTest():
            self.assertIn('spinner-4', td)
        with self.subTest():
            self.assertIn('spinner-1-2', td)
        with self.subTest():
            self.assertIn('spinner-1-2-3', td)
        with self.subTest():
            self.assertIn('spinner-1-2-4', td)
        with self.subTest():
            self.assertIn('spinner-all', td)


    


if __name__ == '__main__':
    unittest.main()