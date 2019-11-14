import os
from flask import Flask, render_template, request, redirect, flash, send_file, url_for
from werkzeug.utils import secure_filename
from common import utils
from common.aws_manager import upload_file, download_file, list_files
from worker import conn
from rq import Queue
from src.main import main

root = utils.get_project_root()
os.makedirs(os.path.join(str(root), 'data', 'videos'), exist_ok=True)
VIDEOS_FOLDER = os.path.join(str(root), 'data', 'videos')
BUCKET = "tubus-system"
ALLOWED_EXTENSIONS = {'avi', 'mov', 'flv', 'mp4'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['VIDEOS_FOLDER'] = VIDEOS_FOLDER

q = Queue(connection=conn, default_timeout=3600)


@app.route('/')
def index():
    return render_template('index.html')


def download_and_process(video_name):
    video = download_file(video_name, BUCKET)
    main(video)  # TODO get the results here, after work is done, data is deleted


def upload(video):
    video.save(os.path.join(app.config['VIDEOS_FOLDER'], video.filename))
    upload_file(os.path.join(app.config['VIDEOS_FOLDER'], video.filename), BUCKET, video.filename)
    return redirect("/storage")


def allowed_video_type(video_name):
    return '.' in video_name and \
           video_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/storage")
def storage():
    videos = list_files("tubus-system")
    return render_template('index.html', videos=videos)


@app.route('/uploading', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        video = request.files['video']
        if video.filename == '':
            flash('No selected video')
            return redirect(request.url)
        if video and allowed_video_type(video.filename):
            flash('Uploading')
            q.enqueue(upload, video, job_id='video_uploading', result_ttl=5000)
            return redirect(request.url)
        else:
            flash('File type not supported')
            return redirect(request.url)


@app.route("/processing/<video_name>", methods=['GET'])
def processing_video(video_name):
    if request.method == 'GET':
        # Background process of video processing
        q.enqueue(download_and_process, video_name, job_id='video_processing', result_ttl=5000)
        # main(video)
        flash('Video is processing')
        return render_template('index.html')


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
        videos = list_files("tubus-system")
        return render_template('index.html', results=results, videos=videos)


if __name__ == "__main__":
    app.run(debug=True)
