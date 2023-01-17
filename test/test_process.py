import unittest
import pandas as pd
import numpy as np
import process
import os


class TestProcess(unittest.TestCase):

    def setUp(self):
        process.GenerateAdjacencyMatrix('test2', 'spinner', 'engdes1', False)

    def tearDown(self):
        try:
            os.remove('./test/data/test2-spinner-engdes1-adjacency.csv')
            os.remove('./test/data/test2-spinner-engdes1.json')
        except:
            pass

    
    def test_add_user_log(self):
        process.AddUserLog({"user": "4321", "exp": "spinner", "hardware":"test00", "course":"tcourse"})
        try:
            line = open('./test/data/4321-test00-spinner-tcourse.json').readline()
        finally:
            os.remove('./test/data/4321-test00-spinner-tcourse.json')

        self.assertEqual(line, '{"user": "4321", "exp": "spinner", "hardware": "test00", "course": "tcourse"}\n')



    
    def test_command_list(self):
        array, last_line = process.GetCommandList('test3', 'spinner', 'engdes1')
        with self.subTest():
            self.assertEqual(len(array), 10)
        with self.subTest():
            self.assertMultiLineEqual(str(last_line), "{'user': 'test3', 't': 1657275054213, 'payload': {'log': 'position', 'data': {'set': 2, 'kp': 1, 'ki': 0, 'kd': 0}}}")

    
    def test_generate_matrix(self):
        #adjacency matrix is generated in setUp
        try:
            df = pd.read_csv('./test/data/test2-spinner-engdes1-adjacency.csv', index_col=0)
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
        process.GenerateAdjacencyMatrix('test2', 'spinner', 'engdes1', False)

        try:
            df = pd.read_csv('./test/data/test2-spinner-engdes1-adjacency.csv', index_col=0)
        except:
            print("csv doesn't exist")

        with self.subTest():
            self.assertEqual(df['voltage_step']['voltage_step'], 2)
        with self.subTest():
            self.assertEqual(df['position_step']['position_step'], 4)
        with self.subTest():
            self.assertEqual(df['position_ramp']['position_ramp'], 6)


    def test_autogenerate_adjacency_0(self):
        mes = {"user": "test", "exp": "spinner", "hardware": "test00", "course":"engdes1", "payload": {"log": "voltage"}}
        # process.AddUserLog(mes)
        process.AutoConvertLogs(mes, 20, False)
        file_exists = os.path.isfile('./test/data/test-spinner-engdes1.csv')
        
        # file should not be created as too few logs
        self.assertFalse(file_exists)

    # test a log file with greater than necessary logs
    def test_autogenerate_adjacency_2(self):
        mes = {"user": "test2", "exp": "spinner", "hardware": "test01", "course":"engdes1", "payload": {"log": "voltage"}}
        # process.AddUserLog(mes)
        process.AutoConvertLogs(mes, 5, False)
        file_exists = os.path.isfile('./test/data/test2-spinner-engdes1-adjacency.csv')
        
        os.remove('./test/data/test2-spinner-engdes1-adjacency.csv')
        
        # file should be created as sufficient logs to run auto generate
        self.assertTrue(file_exists)

    
    def test_command_list_multi_file_0(self):
        
        array, last_line = process.GetCommandList('53a6788c-e689-48d4-9231-c2fbd23df009', 'spinner', 'engdes1')
        #with self.subTest():
        print(array)
        print(last_line)
        self.assertEqual(len(array), 20)
        
    def test_generate_adjacency_multi_file_0(self):
        df = process.GenerateAdjacencyMatrix('53a6788c-e689-48d4-9231-c2fbd23df009', 'spinner', 'engdes1', False)
        
        os.remove('./test/data/53a6788c-e689-48d4-9231-c2fbd23df009-spinner-engdes1-adjacency.csv')
    
        with self.subTest():
            self.assertEqual(df['voltage_step']['voltage_ramp'], 9)
        with self.subTest():
            self.assertEqual(df['voltage_ramp']['voltage_step'], 10)

        

if __name__ == '__main__':
    unittest.main()