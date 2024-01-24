def init():
    global user_timers
    global pomodoro_state
    global pomodoro_time
    global scene_type
    global POMODORO_DEFAULT_TIME
    global LONG_BREAK_MIN
    global SHORT_BREAK_MIN
    global MINUTE
    POMODORO_DEFAULT_TIME = 25 
    LONG_BREAK_MIN = 15
    SHORT_BREAK_MIN = 5
    MINUTE = 60
    user_timers = {}
    scene_type="clock"
    pomodoro_state=False
    pomodoro_time = 0
    
