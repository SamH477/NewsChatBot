from flask import Flask, render_template, request

import speech_recognition as sr


app = Flask(__name__, template_folder='style')

recognizer = sr.Recognizer()
mic = sr.Microphone()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
