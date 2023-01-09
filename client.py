#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
client.py
websocket client for calculating analytics data

Receives logging data by listening to logging websockets. Processes user data into graphs and calculated analytics.
Sends requests for data with a UUID to the connected logging websocket.

Message structure: {user: uuid, t: Date.now(), type: message_type, exp: exp_type, payload: payload}

TESTING by setting up local server and broadcasting
websocat -t ws-l:127.0.0.1:8000 broadcast:mirror:


@author: dprydereid@gmail.com
"""

import json
import os
import _thread
import time
import traceback
import websocket
import analytics
import process
import response
import pandas as pd
from time import sleep

def on_message(ws, message):
    try:
        
        mes = json.loads(message)
        print(mes["type"])
        ## if the message is a logging message from the UI then process this new log
        ## No response sent from client
        if(mes["type"] == "log"):

            process.AddUserLog(mes)

            ## if a student does not access the analytics dashboard then log files will grow without limit.
            ## Automatically convert log files to an adjacency matrix when log file reaches a specific number of lines
            process.AutoConvertLogs(mes, 100)


        ## else if the message is a request to return the analytics for a specific user then do..
        ## user adjacency matrix as a dataframe is generated here and passed to analysis methods
        elif(mes["type"] == "request"):
            user = mes['user']
            exp = mes['exp']
            course = mes['course']
            payload = mes['payload']
            
            A = process.GenerateAdjacencyMatrix(user, exp, course)

            ## if requesting a graph do something
            if(payload['content'] == 'student_graph'):
                res = response.StudentGraphResponse(user, exp, course)
                ws.send(json.dumps(res))
            elif(payload['content'] == 'comparison_graph'):
                res = response.ComparisonGraphResponse(payload['graph'], user, exp)
                ws.send(json.dumps(res))

            ## if requesting task identification do something
            elif(payload['content'] == 'task_identification'):
                res = response.TaskCompletionResponse(A, user, exp, course)
                ws.send(json.dumps(res))
            ##if requesting indicator (e.g. exploration) data do something
            elif(payload['content'] == 'indicators'):
                res = response.IndicatorResponse(A, user, exp, course)
                ws.send(json.dumps(res))

            elif(payload['content'] == 'centroids'):
                res = response.CentroidResponse(A, user, exp, course)
                ws.send(json.dumps(res))

            elif(payload['content'] == 'task_feedback'):
                res = response.TaskFeedbackResponse(A, user, payload['task'], exp, course)
                ws.send(json.dumps(res))
            
            
        ## else if the message is feedback from the user, including tags on the dashboard
        elif(mes["type"] == "feedback"):
            print('logging feedback')
            process.AddUserFeedback(mes)

        elif(mes["type"] == "response"):
            print("Analytics sending response")
        else:
            print("log message not recognised")    
        
    except Exception as e:
        print(e)
        traceback.print_stack()

def connect():
    url = "ws://127.0.0.1:8000"
    #url = "wss://77a0-2a00-23c8-a417-4a01-9ac7-c293-d47-bdc4.ngrok.io"
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print(close_msg) 
    print( "connection lost... reconnecting" )  
    sleep( 2 )
    try:  
        connect()  
        print( "re-connection successful" )  
    except:  
        print( "re-connection NOT successful, retrying in 2 seconds..." )
        

def on_open(ws):
    print('opened')
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())
    

if __name__ == "__main__":
    
    #url = os.environ.get("LOG_URL","ws://127.0.0.1:8888/")
    
    connect()
