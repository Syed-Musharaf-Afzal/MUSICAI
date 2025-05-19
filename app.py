from flask import Flask, render_template, Response, request, jsonify, send_from_directory
import os, random, threading, time, uuid, cv2, numpy as np, pretty_midi
from text_to_music import TextToMusicConverter
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/sounds'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

emotion_dict = {
    0: "Angry", 1: "Disgusted", 2: "Fearful",
    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"
}
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])
model.load_weights('model.h5')

converter = TextToMusicConverter()
detected_emotion = None

@app.route('/')
def index():
    return render_template('index.html')  # unified home

@app.route('/Emotion')
def emotion_page():
    return render_template('Eom.html')

@app.route('/tom')
def text_to_music_page():
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

@app.route('/generate', methods=['POST'])
def generate_music():
    text = request.form.get('text')
    emotion = request.form.get('emotion', 'auto')
    filename = f"output_{uuid.uuid4().hex}.mid"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if emotion == 'auto':
        converter.text_to_music(text, output_file=output_path, play=False)
    else:
        midi = converter.generate_melody(emotion)
        chords = converter.generate_chords(emotion)
        for instrument in chords.instruments:
            midi.instruments.append(instrument)
        midi.write(output_path)
    return jsonify({'success': True, 'file': filename, 'emotion': emotion, 'text': text})

@app.route('/play/<filename>')
def play_midi(filename):
    try:
        midi_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        converter.play_midi(pretty_midi.PrettyMIDI(midi_path))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

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
            roi_gray = gray[y:y+h, x:x+w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img, verbose=0)
            max_index = int(np.argmax(prediction))
            detected_emotion = emotion_dict[max_index]

            # --- Draw thick green rectangle ---
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

            # --- Display emotion ---
            cv2.putText(frame, detected_emotion, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(debug=True)
