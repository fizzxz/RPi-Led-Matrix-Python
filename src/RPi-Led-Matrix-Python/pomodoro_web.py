from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
# from pomodoro_timer import start_pomodoro_sequence,start_timer_thread
from pomodoro_timer import start_timer_thread
import utilities

pomodoro_web_flask = Flask(__name__)
CORS(pomodoro_web_flask)
utilities.init()
global socketio 
socketio= SocketIO(pomodoro_web_flask,ping_interval=0.1,ping_timeout=30)
@pomodoro_web_flask.route("/")
def index():
    return render_template("timer.html")

@pomodoro_web_flask.route('/start_pomodoro_sequence', methods=['POST'])
def start_pomodoro_sequence_route():
    utilities.timer_queue.append({
        "type": "pomodoro",
        "remaining_time": 25*utilities.MINUTE,
        "paused": False,
    })
    utilities.timer_queue.append({
        "type": "break",
        "remaining_time": 5*utilities.MINUTE,
        "paused": False,
    })
    utilities.timer_queue.append({
        "type": "pomodoro",
        "remaining_time": 25*utilities.MINUTE,
        "paused": False,
    })
    utilities.timer_queue.append({
        "type": "break",
        "remaining_time": 5*utilities.MINUTE,
        "paused": False,
    })
    utilities.timer_queue.append({
        "type": "pomodoro",
        "remaining_time": 25*utilities.MINUTE,
        "paused": False,
    })
    utilities.timer_queue.append({
        "type": "break",
        "remaining_time": 15*utilities.MINUTE,
        "paused": False,
    })
    start_timer_thread(socketio)
    return jsonify({'status': 'Pomodoro sequence Added.'})

@pomodoro_web_flask.route("/start_pomodoro", methods=["POST"])
def start_pomodoro():
    utilities.scene_type = "clock"
    duration = int(request.form["duration"])

    utilities.timer_queue.append({
        "type": "pomodoro",
        "remaining_time": duration,
        "paused": False,
    })
    start_timer_thread(socketio)
    return jsonify({"status": "Pomodoro started."})

# Route to start a break timer
@pomodoro_web_flask.route("/start_break", methods=["POST"])
def start_break():
    utilities.scene_type = "clock"
    duration = int(request.form["duration"])

    utilities.timer_queue.append({
        "type": "break",
        "remaining_time": duration,
        "paused": False,
    })
    print(utilities.timer_queue)
    start_timer_thread(socketio)
    return jsonify({"status": "Break started."})

# Route to pause the timer
@pomodoro_web_flask.route("/pause_timer", methods=["POST"])
def pause_timer():
    if utilities.timer_queue[0]["paused"] is False:
        utilities.timer_queue[0]['paused'] = True
        print(utilities.timer_queue[0])
        return jsonify({"status": "Timer paused."})
    else:
        print(utilities.timer_queue)
        return jsonify({"status": "No timer to pause."})

# Route to resume the timer
@pomodoro_web_flask.route("/resume_timer", methods=["POST"])
def resume_timer():
    utilities.scene_type = "clock"
    if utilities.timer_queue[0]["paused"] is True:
        utilities.timer_queue[0]["paused"] = False
        print(utilities.timer_queue[0])
        return jsonify({"status": "Timer resumed."})
    else:
        return jsonify({"status": "No paused timer to resume."})

# Route to remove the timer
@pomodoro_web_flask.route('/remove_timer', methods=['POST'])
def remove_timer():
    if len(utilities.timer_queue)>0:
        utilities.timer_queue[0]["remaining_time"] = 0
        print(utilities.timer_queue[0])
        return jsonify({'status': 'Timer removed.'})
    else:
        return jsonify({'status': 'No active timer to remove.'})

@pomodoro_web_flask.route("/set_weather_scene", methods=["GET"])
def set_weather_scene():
    utilities.scene_type="weather"
    return jsonify({'status': 'Weather Scene Set.'})

@pomodoro_web_flask.route("/set_clock_scene", methods=["GET"])
def set_clock_scene():
    utilities.scene_type="clock"
    return jsonify({'status': 'Clock Scene Set.'})

# SocketIO event to handle getting timer state
@socketio.on('get_timer_state')
def handle_get_timer_state():
    socketio.emit('timer_state', utilities.timer_queue)
    