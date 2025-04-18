from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
import asyncio
from poadcast import Poadcast

app = Flask(__name__)

UPLOAD_FOLDER = "Artifacts"
AUDIO_OUTPUT = "podcast_episode.mp3"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'pdf' not in request.files:
        return "No file part"

    file = request.files['pdf']
    if file.filename == '':
        return "No selected file"

    filename = secure_filename(file.filename)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(pdf_path)

    podcast = Poadcast()
    asyncio.run(podcast.generate_podcast_from_pdf(pdf_path))

    return render_template("index.html", audio=True)

@app.route('/audio')
def audio():
    return send_file(AUDIO_OUTPUT, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
