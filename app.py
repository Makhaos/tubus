import os
from flask import Flask, render_template, request, redirect, make_response, send_file, stream_with_context, Response, \
    jsonify, url_for
from rq.job import Job
from werkzeug.utils import secure_filename
from common import utils
from common.aws_manager import upload_file, download_file, list_files, list_videos
from worker import conn
from rq import Queue
from src.main import main
import logging
import time

root = utils.get_project_root()
os.makedirs(os.path.join(str(root), 'data', 'videos'), exist_ok=True)
VIDEOS_FOLDER = os.path.join(str(root), 'data', 'videos')
BUCKET = "tubus-system"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['VIDEOS_FOLDER'] = VIDEOS_FOLDER

q = Queue(connection=conn, default_timeout=3600)

log = logging.getLogger('tubus')


@app.route('/')
def index():
    videos = list_videos("tubus-system")
    results = list_files("tubus-system")
    return render_template('index.html', videos=videos, results=results)


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

    return make_response(('Chunk upload complete', 200))


@app.route('/processing', methods=['POST'])
def download_and_process(video_name, blur_is_enabled, variance_is_enabled, circles_is_enabled):
    video = download_file(video_name, BUCKET)
    main(video, blur=blur_is_enabled, variance=variance_is_enabled, circles=circles_is_enabled)
    video_name_no_extension, video_name_extension = os.path.splitext(video_name)
    upload_file(os.path.join(str(root), 'data', 'files', video_name_no_extension, 'blur_results.txt'), BUCKET,
                os.path.join(video_name_no_extension + '.txt'))


@app.route("/requesting", methods=['POST'])
def requesting_video():
    video_name = request.form.get('video')
    blur_is_enabled = request.form.get('blur')
    variance_is_enabled = request.form.get('variance')
    circles_is_enabled = request.form.get('circles')
    if blur_is_enabled or variance_is_enabled or circles_is_enabled:
        # Background process of video processing
        q.enqueue(download_and_process, video_name, blur_is_enabled, variance_is_enabled, circles_is_enabled,
                  job_id='video_processing', result_ttl=5000)
        return render_template("loading.html", video_name=video_name, info='is processing', spin='fa-spin')
    return redirect("/")


@app.route("/results", methods=['POST'])
def download_results():
    if request.method == 'POST':
        results = request.form.get('result')
        file = download_file(results, BUCKET)
        return send_file(file,
                         mimetype='text/txt',
                         attachment_filename=results,
                         as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=4034)
