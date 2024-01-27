# from utilities import user_timers
import utilities
import time
import threading          

def update_timers(socketio):
        while True:   
            if len(utilities.timer_queue)>0:
                timer_data=utilities.timer_queue[0]
            if len(utilities.timer_queue)==0:
                return
            
            socketio.emit("timer_state", utilities.timer_queue)
            if timer_data["remaining_time"] > 0 and not timer_data.get("paused", False) and timer_data["type"] =="pomodoro":
                timer_data["remaining_time"] -= 1
                utilities.pomodoro_state = True
                utilities.pomodoro_time = timer_data["remaining_time"]

            if timer_data["remaining_time"] > 0 and not timer_data.get("paused", False) and timer_data["type"] == "break":
                timer_data["remaining_time"] -= 1
                utilities.pomodoro_state = None
                utilities.pomodoro_time = timer_data["remaining_time"]

            if timer_data["remaining_time"] == 0:
                utilities.pomodoro_state = False
                del utilities.timer_queue[0]
                print("Timer Finished") 
            time.sleep(1)
        
def start_timer_thread(socketio):
    timer_thread = threading.Thread(target=update_timers,args=(socketio,))
    timer_thread.start()
