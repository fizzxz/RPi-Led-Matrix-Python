import time


POMODORO_DEFAULT_TIME = 25
LONG_BREAK_MIN = 15
SHORT_BREAK_MIN = 5

def init():
    global user_timers
    global pomodoro_state
    global pomodoro_time
    user_timers = {}
    pomodoro_state=False
    pomodoro_time = 0
    
def start_pomodoro_sequence(user_id):
    # 4 iterations of 25-minute work and 5-minute break
    init()
    for _ in range(4): 
        start_pomodoro_json(POMODORO_DEFAULT_TIME,user_id)
        # add sync instead of sleep 
        time.sleep(POMODORO_DEFAULT_TIME * 60)  
        start_break_json(SHORT_BREAK_MIN,user_id)
        time.sleep(SHORT_BREAK_MIN * 60)  
        
    # On the last iteration, take a longer break
    start_break_json(LONG_BREAK_MIN)
    time.sleep(LONG_BREAK_MIN * 60) 

           
def start_pomodoro_json(duration,user_id):
    user_timers[user_id] = {'type': 'pomodoro', 'duration': duration * 60, 'remaining_time': duration * 60, 'start_time': time.time()}

def start_break_json(duration,user_id):
    user_timers[user_id] = {'type': 'break', 'duration': duration * 60, 'remaining_time': duration * 60, 'start_time': time.time()}