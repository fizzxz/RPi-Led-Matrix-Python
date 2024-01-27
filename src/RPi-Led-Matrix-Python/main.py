#!/usr/bin/env python
import threading
from pomodoro_web import pomodoro_web_flask
from thermometer import updateTempThread
from metoffice.metoffice import get_weather_forecast 
from matrix import matrix_display
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
# from flask_socketio import SocketIO
# Main function
if __name__ == "__main__":
    temperature_thread = threading.Thread(target=updateTempThread)
    temperature_thread.start()

    weather_thread = threading.Thread(target=get_weather_forecast)
    weather_thread.start()
    
    matrix_thread = threading.Thread(target=matrix_display)
    # Set the thread as a daemon
    matrix_thread.daemon = True 
    matrix_thread.start()
    
    # pomodoro_web_flask.run(host="0.0.0.0", port=5000, threaded=True, debug=False)
    # socketio.run(pomodoro_web_flask,host="0.0.0.0", port=5000, debug=False)
    http_server = pywsgi.WSGIServer(('', 5000), pomodoro_web_flask, handler_class=WebSocketHandler)
    http_server.serve_forever()
    if not matrix_thread.process():
        matrix_thread.print_help()
