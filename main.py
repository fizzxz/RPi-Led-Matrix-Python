#!/usr/bin/env python
import time
from datetime import datetime
import json
from temper import Temper, USBList
import threading
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from flask import Flask, Response, request, render_template, jsonify
from flask_cors import CORS

api = Flask(__name__)
app = Flask(__name__)
CORS(app)
# Variable to control the Pomodoro state
pomodoro_running = False

# set matrix options
options = RGBMatrixOptions()
# options.chain_length = 1
options.cols = 64
options.rows = 64
# options.parallel = 1
options.brightness = 15
# options.disable_hardware_pulsing = False
# options.drop_privileges = 1
options.gpio_slowdown = 4
options.hardware_mapping = "adafruit-hat-pwm"
# options.inverse_colors = False
# options.led_rgb_sequence = "RGB"
# options.multiplexing = 0
# options.pixel_mapper_config = ''
options.pwm_bits = 11
# options.pwm_dither_bits = 0
options.pwm_lsb_nanoseconds = 220
# options.row_address_type = 0
# options.scan_mode = 0
options.show_refresh_rate = False
options.limit_refresh_rate_hz = 120
matrix = RGBMatrix(options=options)
class TernaryBoolean:
    def __init__(self, value=None):
        if value in {True, False, None}:
            self.value = value
        else:
            raise ValueError("Invalid value for TernaryBoolean")

    def __repr__(self):
        return str(self.value)

fonts = [
    "fonts/tom-thumb.bdf",
    "fonts/4x6.bdf",
    "fonts/5x7.bdf",
    "fonts/5x8.bdf",
    "fonts/6x9.bdf",
    "fonts/6x10.bdf",
    "fonts/6x12.bdf",
    "fonts/6x13.bdf",
    "fonts/6x13B.bdf",
    "fonts/6x13O.bdf",
    "fonts/8x13.bdf",
    "fonts/8x13B.bdf",
    "fonts/7x13.bdf",
    "fonts/7x14B.bdf",
]
t = Temper()
pomodoro_time = 0
POMODORO_DEFAULT_TIME = 25
LONG_BREAK_MIN = 15
SHORT_BREAK_MIN = 5

pomodoro_state=TernaryBoolean(False)
extTemp = "0.0°C"

user_timers = {}


def start_pomodoro_sequence():

    for _ in range(4):  # 4 iterations of 25-minute work and 5-minute break
        start_timer(POMODORO_DEFAULT_TIME)
        # Wait for the work interval to finish
        time.sleep(POMODORO_DEFAULT_TIME * 60)  
        start_break2(SHORT_BREAK_MIN)
        time.sleep(SHORT_BREAK_MIN * 60)  

    # On the last iteration, take a longer break
    start_break2(LONG_BREAK_MIN)
    time.sleep(LONG_BREAK_MIN * 60) 
           
def start_timer(duration):
    user_id = request.remote_addr
    user_timers[user_id] = {'type': 'pomodoro', 'duration': duration * 60, 'remaining_time': duration * 60, 'start_time': time.time()}

def start_break2(duration):
    user_id = request.remote_addr
    user_timers[user_id] = {'type': 'break', 'duration': duration * 60, 'remaining_time': duration * 60, 'start_time': time.time()}
        
def update_timers():
    global pomodoro_state, pomodoro_time
    while True:
        for user_id, timer_data in list(user_timers.items()):
            
            if timer_data["remaining_time"] > 0 and not timer_data.get("paused", False) and timer_data["type"]=="pomodoro":
                timer_data["remaining_time"] -= 1
                pomodoro_state=True
                pomodoro_time=timer_data["remaining_time"]
                
            if timer_data["remaining_time"] > 0 and not timer_data.get("paused", False) and timer_data["type"]=="break":
                timer_data["remaining_time"] -= 1
                pomodoro_state=None
                pomodoro_time=timer_data["remaining_time"]
                
            if timer_data["remaining_time"] == 0:
                pomodoro_state=False
                user_timers.clear()
                
            time.sleep(1)


# def run_pomodoro(sleep_duration):
#     global pomodoro_running
#     pomodoro_running = True
#     print("Pomodoro started.")
#     time.sleep(sleep_duration * 60)  # Convert minutes to seconds
#     print("Pomodoro completed.")
#     pomodoro_running = False


# def take_break(sleep_duration):
#     print(f"Take a {sleep_duration}-minute break.")
#     time.sleep(sleep_duration * 60)  # Convert minutes to seconds
#     print("Break completed.")


def updateTempThread():
    while True:
        extTemp = updateRoomTemp()
        print("Updated shared value:", extTemp)
        time.sleep(60)


def updateRoomTemp():
    usblist = USBList()
    t.usb_devices = usblist.get_usb_devices()
    result = json.dumps(t.read(), indent=2)

    dataResult = json.loads(result)
    # requires password?
    # print(dataResult)
    # with open("./data.json", "w") as file:
    #     json.dump(result,file,indent=2)
    # with open("./data.json", "r") as file:
    #     rawData = file.read()

    global extTemp
    thermometerData = dataResult

    extTemp = str(thermometerData[0]["external temperature"])
    extTemp = extTemp + "°C"
    return extTemp


def time_collector():
    current_time = datetime.now().strftime("%X")
    return current_time


def date_collector():
    current_date = datetime.today().strftime("%d/%m/%Y")
    return current_date


@app.route("/")
def index():
    return render_template("timer.html")




@app.route('/start_pomodoro_sequence', methods=['POST'])
def start_pomodoro_sequence_route():
    # Start the timer sequence when the button is pressed
    start_pomodoro_sequence()
    return jsonify({'status': 'Pomodoro sequence started.'})

@app.route("/start_pomodoro", methods=["POST"])
def start_pomodoro():
    user_id = request.remote_addr  # Use the user's IP address as a simple identifier
    duration = int(request.form["duration"])

    print(user_id)
    print(user_timers)
    if user_id not in user_timers:
        user_timers[user_id] = {
            "type": "pomodoro",
            "remaining_time": duration * 60,
            "paused": False,
        }
    print(user_timers)
    return jsonify({"status": "Pomodoro started."})


@app.route("/start_break", methods=["POST"])
def start_break():
    user_id = request.remote_addr
    duration = int(request.form["duration"])

    if user_id not in user_timers:
        user_timers[user_id] = {
            "type": "break",
            "remaining_time": duration * 60,
            "paused": False,
        }

    return jsonify({"status": "Break started."})

@app.route("/pause_timer", methods=["POST"])
def pause_timer():
    user_id = request.remote_addr
    timer_data = user_timers.get(user_id)

    if timer_data and not timer_data.get("paused", False):
        timer_data["paused"] = True
        return jsonify({"status": "Timer paused."})
    else:
        return jsonify({"status": "No timer to pause."})


# Add a new route for resuming the timer
@app.route("/resume_timer", methods=["POST"])
def resume_timer():
    user_id = request.remote_addr
    print(user_id)
    timer_data = user_timers.get(user_id)

    if timer_data and timer_data.get("paused", True):
        timer_data["paused"] = False
        return jsonify({"status": "Timer resumed."})
    else:
        return jsonify({"status": "No paused timer to resume."})

@app.route('/remove_timer', methods=['POST'])
def remove_timer():
    global pomodoro_state
    user_id = request.remote_addr

    # Remove the timer for the specified user
    if user_id in user_timers:
        del user_timers[user_id]
        pomodoro_state=False
        return jsonify({'status': 'Timer removed.'})
    else:
        return jsonify({'status': 'No active timer to remove.'})
    
@app.route("/get_timer_state", methods=["GET"])
def get_timer_state():
    user_id = request.remote_addr
    timer_state = user_timers.get(
        user_id, {"type": "", "remaining_time": 0, "paused": False}
    )
    print(timer_state)
    return jsonify(timer_state)


def run():
    temperature_font = graphics.Font()
    temperature_font.LoadFont(fonts[6])
    temperature_colour = graphics.Color(20, 220, 50)
    
    time_font = graphics.Font()
    time_font.LoadFont(fonts[13])
    time_colour = graphics.Color(77, 154, 77)

    calendar_font = graphics.Font()
    calendar_font.LoadFont(fonts[5])
    calendar_colour = graphics.Color(200, 50, 50)
    
    pomodoro_font = graphics.Font()
    pomodoro_font.LoadFont(fonts[13])
    pomodoro_colour = graphics.Color(200, 175, 0)
                                 
    break_font = graphics.Font()
    break_font.LoadFont(fonts[13])
    break_colour = graphics.Color(0, 0, 220)
    
    thread = threading.Thread(target=updateTempThread)
    thread.daemon = True  # Set the thread as a daemon
    thread.start()
    canvas = matrix.CreateFrameCanvas()

    while True:
        canvas.Clear()
        time_on_matrix(canvas,time_font, time_colour)
        date_on_matrix(canvas,calendar_font, calendar_colour)
        temperature_on_matrix(canvas,temperature_font, temperature_colour)
        pomodoro_on_matrix(canvas,pomodoro_font,pomodoro_colour)
        break_on_matrix(canvas,break_font,break_colour)
        # graphics.DrawText(canvas,font,pos,10,textColor,extTemp)
        # time.sleep(0.5)
        # canvas.Clear()
        canvas = matrix.SwapOnVSync(canvas)
        # scheduler.run()

def temperature_on_matrix(canvas,temperature_font, temperature_colour):
    graphics.DrawText(canvas, temperature_font, 11, 57, temperature_colour, extTemp)

def date_on_matrix(canvas,calendar_font, calendar_colour):
    curernt_date = date_collector()
    graphics.DrawText(canvas, calendar_font, 3, 45, calendar_colour, curernt_date)

def time_on_matrix (canvas,time_font, time_colour):
    current_time = time_collector()
    graphics.DrawText(canvas, time_font, 4, 35, time_colour, current_time)
    
def pomodoro_on_matrix(canvas,font,colour):
    # create canvas & content
    global pomodoro_state, pomodoro_time     

    if pomodoro_state is True:
        graphics.DrawText(canvas, font, 15, 20, colour, convert_seconds(pomodoro_time))

def break_on_matrix(canvas,font,colour):
    # create canvas & content
    global pomodoro_state, pomodoro_time     
    if pomodoro_state is None:
        graphics.DrawText(canvas, font, 15, 20, colour, convert_seconds(pomodoro_time))            
        
def convert_seconds(total_seconds):
  """Converts seconds to minutes and seconds in a formatted string."""
  minutes = int(total_seconds // 60)
  seconds = int(total_seconds % 60)
  return f"{minutes:02d}:{seconds:02d}"  # Formatted output with leading zeros
            


# def run_api():
#     api.run(debug=True)
# Main function
if __name__ == "__main__":
    run_text_thread = threading.Thread(target=run)
    run_text_thread.start()
    # Start the timer update thread
    timer_thread = threading.Thread(target=update_timers)
    timer_thread.start()
    # timer_thread1 = threading.Thread(target=start_pomodoro_sequence)
    # timer_thread1.start()
  
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=False)
    # api.run(host="0.0.0.0", port=5000, threaded=True, debug=False)
    # api.run(debug=False)
    # run_text = run()
    if not run_text_thread.process():
        run_text_thread.print_help()
