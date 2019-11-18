import os
from flask import Flask, render_template, request, redirect, flash, send_file, url_for, make_response
from rq.job import Job
from werkzeug.utils import secure_filename
from common import utils
from common.aws_manager import upload_file, download_file, list_files
from worker import conn
from rq import Queue
from src.main import main
import logging
import time

root = utils.get_project_root()
os.makedirs(os.path.join(str(root), 'data', 'videos'), exist_ok=True)
VIDEOS_FOLDER = os.path.join(str(root), 'data', 'videos')
BUCKET = "tubus-system"
ALLOWED_EXTENSIONS = {'avi', 'mov', 'flv', 'mp4'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['VIDEOS_FOLDER'] = VIDEOS_FOLDER

q = Queue(connection=conn, default_timeout=3600)

log = logging.getLogger('pydrop')


@app.route('/')
def index():
    return render_template('index.html')


def download_and_process(video_name):
    video = download_file(video_name, BUCKET)
    main(video)


def video_type(video_name):
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
        if video and video_type(video.filename):
            video.save(os.path.join(app.config['VIDEOS_FOLDER'], video.filename))
            flash('Uploading')
            upload_file(os.path.join(app.config['VIDEOS_FOLDER'], video.filename), BUCKET, video.filename)
            return redirect("/storage")
        else:
            flash('File type not supported')
            return redirect(request.url)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    save_path = os.path.join(app.config['VIDEOS_FOLDER'], secure_filename(file.filename))
    current_chunk = int(request.form['dzchunkindex'])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if os.path.exists(save_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
        return make_response(('File already exists', 400))

    try:
        with open(save_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(file.stream.read())
            upload_file(save_path, BUCKET, secure_filename(file.filename))
    except OSError:
        # log.exception will include the traceback so we can see what's wrong
        log.exception('Could not write to file')
        return make_response(("Not sure why,"
                              " but we couldn't write the file to disk", 500))

    total_chunks = int(request.form['dztotalchunkcount'])

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
            log.error(f"File {file.filename} was completed, "
                      f"but has a size mismatch."
                      f"Was {os.path.getsize(save_path)} but we"
                      f" expected {request.form['dztotalfilesize']} ")
            return make_response(('Size mismatch', 500))
        else:
            log.info(f'File {file.filename} has been uploaded successfully')
    else:
        log.debug(f'Chunk {current_chunk + 1} of {total_chunks} '
                  f'for file {file.filename} complete')

    return make_response(("Chunk upload successful", 200))


@app.route("/processing/<video_name>", methods=['GET'])
def processing_video(video_name):
    if request.method == 'GET':
        # Background process of video processing
        background_process = q.enqueue(download_and_process, video_name, job_id='video_processing', result_ttl=5000)
        flash('Video is processing')
        return render_template('index.html'), job_status(video_name)


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


def job_status(video_name):
    job = Job.fetch('video_processing', connection=conn)
    while True:
        job.refresh()
        print(job.get_id(), job.get_status(), job.meta.get('word'))
        if job.is_finished:
            with open(os.path.join(str(root), 'data', 'files', video_name, 'blur_results.txt'), 'r') as reader:
                results = reader
            videos = list_files("tubus-system")
            return render_template('index.html', results=results, videos=videos)
        else:
            flash('Video is processing')
            time.sleep(5)
            return render_template('index.html'), job_status(video_name)


if __name__ == "__main__":
    app.run(debug=True)
