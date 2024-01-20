
# from utilities import user_timers
import utilities
import time


utilities.init()
def update_timers():
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
                utilities.user_timers.clear()
            
            time.sleep(1)
            
            

