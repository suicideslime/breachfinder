from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from typing import List, Dict
from threading import Thread
from config import Config
from worker import CredentialWorker
from credential_checker import Credential
from logger import Logger
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class WebWorker:
    def __init__(self):
        self.current_job = None
        self.results: List[Dict] = []
        self.progress = 0
        self.total = 0
        self.is_running = False
        self.logger = Logger("logs/web.log")

    def start_job(self, config: Config):
        if self.is_running:
            return False
        
        self.is_running = True
        self.progress = 0
        self.results = []
        
        thread = Thread(target=self._run_job, args=(config,))
        thread.daemon = True
        thread.start()
        return True

    def _run_job(self, config: Config):
        try:
            worker = CredentialWorker(config)
            credentials = []

            with open(config.input_file, 'r') as file:
                for line in file:
                    credential = Credential.from_line(line)
                    if credential:
                        credentials.append(credential)

            self.total = len(credentials)
            if self.total == 0:
                self.logger.warning("No valid credentials found in file")
                return

            valid_credentials = worker.process_credentials(credentials)
            
            if valid_credentials:
                os.makedirs(os.path.dirname(config.output_file), exist_ok=True)
                with open(config.output_file, 'w') as valid_file:
                    for credential in valid_credentials:
                        valid_file.write(credential.to_line() + '\n')
                        self.results.append({
                            'url': credential.url,
                            'username': credential.username,
                            'status': 'Valid'
                        })

        except Exception as e:
            self.logger.error(f"Job error: {str(e)}")
        finally:
            self.is_running = False

web_worker = WebWorker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        config = Config(
            input_file=filepath,
            output_file=f"results/{filename}_valid.txt",
            num_threads=int(request.form.get('threads', 4)),
            requests_per_second=int(request.form.get('rate_limit', 2))
        )
        
        if web_worker.start_job(config):
            return jsonify({'message': 'Job started successfully'})
        else:
            return jsonify({'error': 'Job already running'}), 400

@app.route('/status')
def get_status():
    return jsonify({
        'is_running': web_worker.is_running,
        'progress': web_worker.progress,
        'total': web_worker.total,
        'results': web_worker.results
    })

@app.route('/results')
def download_results():
    if os.path.exists('results/valid.txt'):
        return send_file('results/valid.txt', as_attachment=True)
    return jsonify({'error': 'No results available'}), 404

if __name__ == '__main__':
    app.run(debug=True) 