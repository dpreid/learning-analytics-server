import unittest
import pandas as pd
import numpy as np
import process
import os


class TestProcess(unittest.TestCase):

    def test_add_user_log(self):
        process.AddUserLog({"user": "4321", "exp": "spinner"})
        try:
            line = open('./test/data/4321-spinner.json').readline()
        finally:
            os.remove('./test/data/4321-spinner.json')

        self.assertEqual(line, '{"user": "4321", "exp": "spinner"}\n')


    def test_command_list(self):
        array = process.GetCommandList('1234', 'spinner')
        self.assertEqual(len(array), 10)

    def test_generate_matrix(self):
        process.GenerateAdjacencyMatrix('1234', 'spinner', False)

        try:
            df = pd.read_csv('./test/data/1234-spinner-adjacency.csv', index_col=0)
        finally:
            os.remove('./test/data/1234-spinner-adjacency.csv')

        with self.subTest():
            self.assertEqual(df['voltage_step']['voltage_step'], 1)
        with self.subTest():
            self.assertEqual(df['position_step']['position_step'], 2)
        with self.subTest():
            self.assertEqual(df['position_ramp']['position_ramp'], 3)

    def test_generate_matrix_with_existing_matrix(self):
        process.GenerateAdjacencyMatrix('1234', 'spinner', False)
        process.GenerateAdjacencyMatrix('1234', 'spinner', False)

        try:
            df = pd.read_csv('./test/data/1234-spinner-adjacency.csv', index_col=0)
        finally:
            os.remove('./test/data/1234-spinner-adjacency.csv')

        with self.subTest():
            self.assertEqual(df['voltage_step']['voltage_step'], 2)
        with self.subTest():
            self.assertEqual(df['position_step']['position_step'], 4)
        with self.subTest():
            self.assertEqual(df['position_ramp']['position_ramp'], 6)

    
    # def test_draw_graph(self):
    #     process.GenerateAdjacencyMatrix('1234', 'spinner', False)
    #     process.DrawGraph('1234', 'spinner')
    #     os.remove('./test/data/1234-spinner-adjacency.csv')


if __name__ == '__main__':
    unittest.main()