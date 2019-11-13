import os
from flask import Flask, render_template, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
from common import utils
from worker import conn
from rq import Queue
from src.main import main

root = utils.get_project_root()
os.makedirs(os.path.join(str(root), 'data', 'videos'), exist_ok=True)
UPLOAD_FOLDER = os.path.join(str(root), 'data', 'videos')
ALLOWED_EXTENSIONS = {'avi', 'mov', 'flv', 'mp4'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Database SQlite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tubus.db'
# db = SQLAlchemy(app)

q = Queue(connection=conn, default_timeout=3600)


@app.route('/')
def index():
    return render_template('index.html')


def allowed_video_type(videoname):
    return '.' in videoname and \
           videoname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploading', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No video part')
            return redirect(request.url)
        video = request.files['video']
        if video.filename == '':
            flash('No selected video')
            return redirect(request.url)
        if video and allowed_video_type(video.filename):
            videoname = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], videoname))
            video_name_no_extension, video_name_extension = os.path.splitext(videoname)
            # Background process of video processing
            background_process = q.enqueue(main, job_id='video_processing', result_ttl=5000)
            flash('Video is processing')
            job_id = background_process.get_id()
            results = video_name_no_extension
        else:
            flash('File type not supported')
            return redirect(request.url)
        return render_template('index.html', results=results)


@app.route('/results', methods=['POST'])
def show_results():
    if request.method == 'POST':
        if os.path.exists(os.path.join(str(root), 'data')):
            print('data exists')
            results = 'data exists'
            if os.path.exists(os.path.join(str(root), 'data', 'files')):
                print('files exists')
                results = 'files exists'
            else:
                print('there are no files')
                results = 'there are no files'
        else:
            print('there is no data')
            results = 'there is no data'
        return render_template('index.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
