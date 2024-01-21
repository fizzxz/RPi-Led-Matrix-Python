#!/usr/bin/env python
import threading
from pomodoro_web import pomodoro_web_flask
from pomodoro_timer import start_timer_thread
from thermometer import updateTempThread
from matrix import matrix_display



# Main function
if __name__ == "__main__":

    matrix_thread = threading.Thread(target=matrix_display)
    # Set the thread as a daemon
    matrix_thread.daemon = True 
    matrix_thread.start()
    # start_timer_thread()
    temperature_thread = threading.Thread(target=updateTempThread)
    temperature_thread.start()
  
    pomodoro_web_flask.run(host="0.0.0.0", port=5000, threaded=True, debug=False)

    if not matrix_thread.process():
        matrix_thread.print_help()
