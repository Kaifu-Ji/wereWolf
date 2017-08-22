from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def play():
    return render_template("audio_test.html")

app.run(host="0.0.0.0",port=8000)