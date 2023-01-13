import unittest
import pandas as pd
import numpy as np
import process
import analytics
import os


class TestResponse(unittest.TestCase):

    def setUp(self):
        self.A = process.GenerateAdjacencyMatrix('analytics', 'spinner', 'cie3', False)

    def tearDown(self):
        try:
            os.remove('./test/data/analytics-spinner-cie3-adjacency.csv')
        except:
            pass
    @unittest.skip
    def test_taskidentification(self):
        td = analytics.TaskIdentification(self.A, 'spinner', 'cie3')
        with self.subTest():
            self.assertIn('spinner-cie3-3', td)
        with self.subTest():
            self.assertIn('spinner-cie3-4', td)
        with self.subTest():
            self.assertIn('spinner-cie3-1-2', td)
        with self.subTest():
            self.assertIn('spinner-cie3-1-2-3', td)
        with self.subTest():
            self.assertIn('spinner-cie3-1-2-4', td)
        with self.subTest():
            self.assertIn('spinner-cie3-all', td)


    


if __name__ == '__main__':
    unittest.main()