import unittest
import pandas as pd
import numpy as np
import process
import os


class TestProcess(unittest.TestCase):

    def setUp(self):
        process.GenerateAdjacencyMatrix('1234', 'spinner', False)

    def tearDown(self):
        try:
            os.remove('./test/data/1234-spinner-adjacency.csv')
        except:
            pass


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
        
        try:
            df = pd.read_csv('./test/data/1234-spinner-adjacency.csv', index_col=0)
        except:
            print("csv doesn't exist")
            

        with self.subTest():
            self.assertEqual(df['voltage_step']['voltage_step'], 1)
        with self.subTest():
            self.assertEqual(df['position_step']['position_step'], 2)
        with self.subTest():
            self.assertEqual(df['position_ramp']['position_ramp'], 3)



    def test_generate_matrix_with_existing_matrix(self):
        # generate matrix a second time
        process.GenerateAdjacencyMatrix('1234', 'spinner', False)

        try:
            df = pd.read_csv('./test/data/1234-spinner-adjacency.csv', index_col=0)
        except:
            print("csv doesn't exist")

        with self.subTest():
            self.assertEqual(df['voltage_step']['voltage_step'], 2)
        with self.subTest():
            self.assertEqual(df['position_step']['position_step'], 4)
        with self.subTest():
            self.assertEqual(df['position_ramp']['position_ramp'], 6)

    
    def test_draw_graph_html(self):
        process.DrawGraphHTML('1234', 'spinner')

    # def test_draw_graph_image(self):
    #     process.DrawGraphImage('1234', 'spinner')


if __name__ == '__main__':
    unittest.main()