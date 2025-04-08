from flask import Flask, render_template, Response, request, jsonify
import numpy as np
import cv2
import os
import random
import threading
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env file!")

# Flask app setup
app = Flask(__name__)

# Hugging Face config
API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Emotion model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))
model.load_weights('model.h5')

emotion_dict = {
    0: "Angry", 1: "Disgusted", 2: "Fearful",
    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"
}
detected_emotion = None

def generate_frames():
    global detected_emotion
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            max_index = int(np.argmax(prediction))
            detected_emotion = emotion_dict[max_index]
            cv2.putText(frame, detected_emotion, (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

# ===================== Routes ======================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Emotion')
def eom():
    return render_template('Eom.html')

@app.route('/tom')
def tom():
    return render_template('tom.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect_emotion', methods=['GET'])
def detect_emotion():
    global detected_emotion
    if detected_emotion:
        emotion = detected_emotion
        detected_emotion = None

        music_folder = os.path.join("static", "songs", emotion.lower())
        if not os.path.exists(music_folder) or not os.listdir(music_folder):
            return jsonify({'emotion': emotion, 'status': f'No songs available for {emotion}', 'song': None})

        song_name = random.choice(os.listdir(music_folder))
        song_path = f"/static/songs/{emotion.lower()}/{song_name}"

        return jsonify({'emotion': emotion, 'status': f'Music selected for {emotion}', 'song': song_path})

    return jsonify({'emotion': None, 'status': 'No emotion detected', 'song': None})

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt")

    if not prompt:
        return jsonify({"status": "error", "message": "Prompt is required."})

    payload = {"inputs": prompt}  # ONLY send prompt!

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)

            if response.status_code == 503:
                return jsonify({"status": "error", "message": "Model is loading. Try again."})
            elif response.status_code == 401:
                return jsonify({"status": "error", "message": "Invalid Hugging Face token."})
            elif response.status_code == 500:
                return jsonify({"status": "error", "message": "Internal server error from Hugging Face. Prompt might be too complex or model crashed."})
            elif response.status_code != 200:
                return jsonify({"status": "error", "message": f"API error {response.status_code}: {response.text}"})

            audio_data = response.content
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"static/music_{timestamp}.wav"
            with open(filename, "wb") as f:
                f.write(audio_data)

            return jsonify({"status": "success", "file": filename})
        except Exception as e:
            return jsonify({"status": "error", "message": f"Exception: {str(e)}"})

    return jsonify({"status": "error", "message": "Model too busy. Try later."})

# ===================== Run ======================

if __name__ == "__main__":
    app.run(debug=True)
