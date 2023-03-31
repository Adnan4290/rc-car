from flask import Flask, render_template, Response
from camera_stream import gen_frames
from input_handler import handle_input
from flask_socketio import SocketIO, send, emit
import atexit,cv2
app = Flask(__name__)
app.debug=True
socketio = SocketIO(app)

latitude=None
longitude=None
# Release the camera when the Flask app is shut down
def release_camera():
    global cap
    cap.release()

@app.before_first_request
def before_first_request():
    global cap
    cap = cv2.VideoCapture(0)
    app.logger.info('Camera opened')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    message = handle_input()
    print(message)
    return message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/switch_camera', methods=['POST','GET'])
def switchcamera():
    print("switch camera route accessed")
    # Call the function to switch cameras
    # switch_camera()
    return "switch camera route finished running"

# code for displaying latitude and longitude 
@app.route('/latitude')
def get_latitude():
    global latitude
    return str(latitude)

# endpoint to get the longitude value
@app.route('/longitude')
def get_longitude():
    global longitude
    return str(longitude)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def send_frame(frame):
    emit('frame', frame)

if __name__ == '__main__':
    atexit.register(release_camera)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
