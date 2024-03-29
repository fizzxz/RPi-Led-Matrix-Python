from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from pomodoro_timer import start_pomodoro_sequence,start_timer_thread
import utilities
import threading
pomodoro_web_flask = Flask(__name__)
CORS(pomodoro_web_flask)
utilities.init()

@pomodoro_web_flask.route("/")
def index():
    return render_template("timer.html")

@pomodoro_web_flask.route('/start_pomodoro_sequence', methods=['POST'])
def start_pomodoro_sequence_route():
    user_id = request.remote_addr  # Use the user's IP address as a simple identifier
    timer_thread = threading.Thread(target=start_pomodoro_sequence,args=(user_id,))
    timer_thread.start()  
    return jsonify({'status': 'Pomodoro sequence started.'})

@pomodoro_web_flask.route("/start_pomodoro", methods=["POST"])
def start_pomodoro():
    start_timer_thread()
    utilities.scene_type = "clock"
    user_id = request.remote_addr  # Use the user's IP address as a simple identifier
    duration = int(request.form["duration"])

    if user_id not in utilities.user_timers:
        utilities.user_timers[user_id] = {
            "type": "pomodoro",
            "remaining_time": duration,
            "paused": False,
        }
    print(utilities.user_timers)
    return jsonify({"status": "Pomodoro started."})

@pomodoro_web_flask.route("/start_break", methods=["POST"])
def start_break():
    start_timer_thread()
    utilities.scene_type = "clock"
    user_id = request.remote_addr
    duration = int(request.form["duration"])

    if user_id not in utilities.user_timers:
        utilities.user_timers[user_id] = {
            "type": "break",
            "remaining_time": duration,
            "paused": False,
        }
    print(utilities.user_timers)
    return jsonify({"status": "Break started."})

@pomodoro_web_flask.route("/pause_timer", methods=["POST"])
def pause_timer():
    user_id = request.remote_addr
    timer_data = utilities.user_timers.get(user_id)
    if timer_data and not timer_data.get("paused", False):
        timer_data["paused"] = True
        print(timer_data)
        return jsonify({"status": "Timer paused."})
    else:
        print(timer_data)
        return jsonify({"status": "No timer to pause."})

@pomodoro_web_flask.route("/resume_timer", methods=["POST"])
def resume_timer():
    user_id = request.remote_addr
    timer_data = utilities.user_timers.get(user_id)
    utilities.scene_type = "clock"
    if timer_data and timer_data.get("paused", True):
        timer_data["paused"] = False
        return jsonify({"status": "Timer resumed."})
    else:
        return jsonify({"status": "No paused timer to resume."})

@pomodoro_web_flask.route('/remove_timer', methods=['POST'])
def remove_timer():
    user_id = request.remote_addr
    timer_data = utilities.user_timers.get(user_id)
    if user_id in utilities.user_timers:
        timer_data["remaining_time"] = 0
        return jsonify({'status': 'Timer removed.'})
    else:
        return jsonify({'status': 'No active timer to remove.'})
    
@pomodoro_web_flask.route("/get_timer_state", methods=["GET"])
def get_timer_state():
    user_id = request.remote_addr
    timer_state = utilities.user_timers.get(
        user_id, {"type": "", "remaining_time": 0, "paused": False}
    )

    return jsonify(timer_state)

@pomodoro_web_flask.route("/set_weather_scene", methods=["GET"])
def set_weather_scene():
    utilities.scene_type="weather"
    return jsonify({'status': 'Weather Scene Set.'})

@pomodoro_web_flask.route("/set_clock_scene", methods=["GET"])
def set_clock_scene():
    utilities.scene_type="clock"
    return jsonify({'status': 'Clock Scene Set.'})