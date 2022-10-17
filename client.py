#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
client.py
websocket client for calculating analytics data

Receives logging data by listening to logging websockets. Processes user data into graphs and calculated analytics.
Sends requests for data with a UUID to the connected logging websocket.

@author: dprydereid@gmail.com
"""

import json
import os
import _thread
import time
import traceback
import websocket

def on_message(ws, message):
    
    try:

        mes = json.loads(message)

        ## if the message is a logging message from the UI then process this new log
        if(mes["type"] == "log"):
            print("logging")

        ## else if the message is a request to return the analytics for a specific user then do..
        elif(mes["type"] == "request"):
            print("request")
            ## temp for now
            result = mes
            ws.send(json.dumps(result))    

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
    
    url = os.environ.get("SESSION_URL","ws://172.17.0.1:8888/ws/calibration")

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(url,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
