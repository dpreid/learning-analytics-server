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

def on_message(ws, message):
    print("on_message")
    try:

        mes = json.loads(message)

        ## if the message is a logging message from the UI then process this new log
        ## No response sent from client
        if(mes["type"] == "log"):

            process.AddUserLog(mes)


        ## else if the message is a request to return the analytics for a specific user then do..
        ## user adjacency matrix as a dataframe is generated here and passed to analysis methods
        elif(mes["type"] == "request"):
            user = mes['user']
            exp = mes['exp']
            ##update this to reflect use of a single method to generate analytics
            A = process.GenerateAdjacencyMatrix(user, exp)

            ## if requesting a graph do something

            ## if requesting task identification do something

            ##if requesting exploration data do something


            res = response.TestResponse(A, user, exp)
            
            ws.send(json.dumps(res))
            
        ## else if the message is feedback from the user, including tags on the dashboard
        elif(mes["type"] == "feedback"):
            res = {"type": "success", "response": "feedback_received"}
            ws.send(json.dumps(res)) 

        else:
            print("log message not recognised")    
        
    except Exception as e:
        print(e)
        traceback.print_stack()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    
    #url = os.environ.get("SESSION_URL","ws://127.0.0.1:8888/")
    url = "ws://127.0.0.1:8000"

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)

    ws.run_forever()
