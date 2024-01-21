
# from utilities import user_timers
import utilities
import time
import threading

def update_timers():
    utilities.init()
    while True:
        for user_id,timer_data in list(utilities.user_timers.items()):
            if timer_data["remaining_time"] > 0 and not timer_data.get("paused", False) and timer_data["type"]=="pomodoro":
                timer_data["remaining_time"] -= 1
                utilities.pomodoro_state=True
                utilities.pomodoro_time=timer_data["remaining_time"]
                
            if timer_data["remaining_time"] > 0 and not timer_data.get("paused", False) and timer_data["type"]=="break":
                timer_data["remaining_time"] -= 1
                utilities.pomodoro_state=None
                utilities.pomodoro_time=timer_data["remaining_time"]
                
            if timer_data["remaining_time"] == 0:
                utilities.pomodoro_state=False
                del utilities.user_timers[user_id]
                print("Timer Finished")
                return
            
            time.sleep(1)
    
# def create_thread():
def start_timer_thread():
    timer_thread = threading.Thread(target=update_timers)
    timer_thread.start()         
            
def start_pomodoro_sequence(user_id):
    # 4 iterations of 25-minute work and 5-minute break
    utilities.init()
    for _ in range(4): 
        timer_thread = threading.Thread(target=update_timers)
        timer_thread.start()    
        start_pomodoro_json(utilities.POMODORO_DEFAULT_TIME,user_id)
        while timer_thread.is_alive():
            pass    
        
        timer_thread1 = threading.Thread(target=update_timers)
        timer_thread1.start()    
        start_break_json(utilities.SHORT_BREAK_MIN,user_id)
        while timer_thread1.is_alive():
            pass

    # On the last iteration, take a longer break
    timer_thread2 = threading.Thread(target=update_timers)
    timer_thread2.start()    
    start_break_json(utilities.LONG_BREAK_MIN,user_id)
    while timer_thread2.is_alive():
        pass
           
def start_pomodoro_json(duration,user_id):
    utilities.user_timers[user_id] = {'type': 'pomodoro', 'duration': duration * utilities.MINUTE, 'remaining_time': duration * utilities.MINUTE, 'start_time': time.time()}

def start_break_json(duration,user_id):
    utilities.user_timers[user_id] = {'type': 'break', 'duration': duration * utilities.MINUTE, 'remaining_time': duration * utilities.MINUTE, 'start_time': time.time()}            

