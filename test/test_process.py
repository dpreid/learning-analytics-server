import unittest
import pandas as pd
import numpy as np
import process
import os


class TestProcess(unittest.TestCase):

    def setUp(self):
        process.GenerateAdjacencyMatrix('1234', 'spinner', 'tcourse', False)

    def tearDown(self):
        try:
            os.remove('./test/data/1234-spinner-tcourse-adjacency.csv')
        except:
            pass


    def test_add_user_log(self):
        process.AddUserLog({"user": "4321", "exp": "spinner", "course":"tcourse"})
        try:
            line = open('./test/data/4321-spinner-tcourse.json').readline()
        finally:
            os.remove('./test/data/4321-spinner-tcourse.json')

        self.assertEqual(line, '{"user": "4321", "exp": "spinner", "course": "tcourse"}\n')




    def test_command_list(self):
        array, last_line = process.GetCommandList('1234', 'spinner', 'tcourse')
        with self.subTest():
            self.assertEqual(len(array), 10)
        with self.subTest():
            self.assertMultiLineEqual(last_line, '{"user": "expert", "t": 1657275054213, "payload": {"log": "position", "data": {"set": 2, "kp": 1, "ki": 0, "kd": 0}}} \n')


    def test_generate_matrix(self):
        
        try:
            df = pd.read_csv('./test/data/1234-spinner-tcourse-adjacency.csv', index_col=0)
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
        process.GenerateAdjacencyMatrix('1234', 'spinner', 'tcourse', False)

        try:
            df = pd.read_csv('./test/data/1234-spinner-tcourse-adjacency.csv', index_col=0)
        except:
            print("csv doesn't exist")

        with self.subTest():
            self.assertEqual(df['voltage_step']['voltage_step'], 2)
        with self.subTest():
            self.assertEqual(df['position_step']['position_step'], 4)
        with self.subTest():
            self.assertEqual(df['position_ramp']['position_ramp'], 6)

    
    def test_draw_graph_html(self):
        process.SaveGraphHTML('1234', 'spinner', 'tcourse')

    # def test_draw_graph_image(self):
    #     process.DrawGraphImage('1234', 'spinner')

    # test an empty log file
    def test_autogenerate_adjacency_0(self):
        mes = {"user": "test0", "exp": "spinner", "course":"cie3", "payload": {"log": "voltage"}}
        # process.AddUserLog(mes)
        process.AutoConvertLogs(mes, 20)
        file_exists = os.path.isfile('./test/data/test0-spinner-cie3.csv')
        
        #os.remove('./test/data/test0-spinner-cie3.csv')
        
        # file should not be created as too few logs
        self.assertFalse(file_exists)

    # test a log file with fewer than necessary logs
    def test_autogenerate_adjacency_1(self):
        mes = {"user": "test1", "exp": "spinner", "course":"cie3", "payload": {"log": "voltage"}}
        # process.AddUserLog(mes)
        process.AutoConvertLogs(mes, 20)
        file_exists = os.path.isfile('./test/data/test1-spinner-cie3.csv')
        
        #os.remove('./test/data/test0-spinner-cie3.csv')
        
        # file should not be created as too few logs
        self.assertFalse(file_exists)

    # test a log file with greater than necessary logs
    def test_autogenerate_adjacency_2(self):
        mes = {"user": "test2", "exp": "spinner", "course":"cie3", "payload": {"log": "voltage"}}
        # process.AddUserLog(mes)
        process.AutoConvertLogs(mes, 20, False)
        file_exists = os.path.isfile('./test/data/test2-spinner-cie3-adjacency.csv')
        
        os.remove('./test/data/test2-spinner-cie3-adjacency.csv')
        
        # file should be created as sufficient logs to run auto generate
        self.assertTrue(file_exists)


if __name__ == '__main__':
    unittest.main()