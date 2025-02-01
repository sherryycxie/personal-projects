from flask import Flask, render_template, request, jsonify
import os
import sqlite3
from werkzeug.utils import secure_filename
from utils.transcriber import transcribe_audio
from utils.summarizer import summarize_text
from openai import OpenAI

# Configure OpenAI API client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/audio_uploads'
DATABASE = 'summaries.db'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                transcription TEXT,
                summary TEXT
            )
        ''')
        conn.commit()

init_db()

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a'}
ALLOWED_MIMETYPES = {
    'audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/mp4',
    'audio/x-m4a', 'audio/aac', 'video/mp4'
}

def allowed_file(filename):
    """Check if the file is allowed based on extension and MIME type."""
    extension_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if not extension_allowed:
        return False
    if request.files['audio_file'].content_type.lower() not in ALLOWED_MIMETYPES:
        app.logger.warning(f"Invalid MIME type: {request.files['audio_file'].content_type}")
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        transcript = transcribe_audio(filepath)
        summary = summarize_text(client, transcript)

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO summaries (transcription, summary) VALUES (?, ?)", (transcript, summary))
            conn.commit()

        os.remove(filepath)

        return render_template('result.html', transcript=transcript, summary=summary)
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': str(e)}), 500

"""
@app.route('/summaries', methods=['GET']) Defines an API Endpoint 
When a user visits /summaries, Flask fetches all stored summaries from summaries.db through the following function
"""
@app.route('/summaries', methods=['GET'])
def get_summaries():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, transcription, summary FROM summaries ORDER BY timestamp DESC")
            summaries = cursor.fetchall()
        return jsonify([{'id': row[0], 'timestamp': row[1], 'transcription': row[2], 'summary': row[3]} for row in summaries])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)