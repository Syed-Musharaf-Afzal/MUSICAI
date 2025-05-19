# 🎵 Emotion-Based & Text-to-Music Generation App

This is a full-stack web application that combines **real-time emotion detection** and **AI-based music generation** using text prompts. Built with a Flask backend and HTML/CSS/JavaScript frontend, the app delivers a unique musical experience either based on your mood or your imagination!

## 🚀 Features

- 🎭 Real-time **emotion detection** using webcam
- 🎧 **Emotion-based music playback** from local categorized songs
- 🧠 Generate music from **text prompts** using Hugging Face’s `facebook/musicgen-small` model
- 🎛️ Interactive music controls (play, pause, forward, volume)
- 🌐 Frontend built with HTML, CSS, JavaScript, and Bootstrap
- 🔙 Backend powered by Flask (Python 3.10)
- 🔒 Hugging Face Inference API integration with API key support

---

## 🧠 How It Works

### 🎭 Emotion-Based Music Playback

1. User allows webcam access.
2. A pre-trained model detects the user's facial emotion.
3. Based on the detected emotion (Happy, Sad, Angry, etc.), music is selected from categorized folders and played.

### 🎧 Text-to-Music Generation

1. User enters a **text prompt** (e.g., *"calm evening by the lake"*) and selects a **duration**.
2. The backend calls Hugging Face’s `facebook/musicgen-small` model via API.
3. Generated music is streamed and played in the browser.

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Syed-Musharaf-Afzal/MUSICAI.git
cd MusicAI
```

### 2. Install Dependencies

Create a virtual environment and install requirements:

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Hugging Face API Key

Create a `.env` file:

```bash
HUGGINGFACE_API_KEY=your_api_key_here
```

### 4. Run the App

```bash
python app.py
```

The app will run at `http://127.0.0.1:5000`.

---

## 🧪 Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python 3.12, Flask, Tensorflow
- **AI Models**:
  - Emotion Detection: Custom pre-trained model (OpenCV/Dlib or similar)
  - Music Generation: Hugging Face `facebook/musicgen-small`

---

## 📦 Requirements

- Python 3.7+,3.12+
- 8 GB+ RAM
- Hugging Face API key (free tier works fine)

---

## 🙌 Credits

- [Hugging Face Transformers](https://huggingface.co/facebook/musicgen-small)
- [Bootstrap](https://getbootstrap.com/)
- Emotion detection model based on OpenCV / Dlib / Haarcascade

---

## 🎓 About Code Unnati

This project is developed under the Code Unnati Capstone Project — a digital skilling initiative by Edunet Foundation, supported by SAP. Learn more: https://codeunnati.edunetfoundation.com

---

## 🤝 Contributors

Syed Musharaf Afzal, Mohammed Hamza Hussain, Mohd Osman

NSAKCET – Institutional Support

Edunet Foundation – Capstone Mentorship

---

## 📄 License

This project is for educational purposes under the Code Unnati Capstone Program.
