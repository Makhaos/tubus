import os
from flask import Flask, render_template, request, redirect, make_response, Response
from werkzeug.utils import secure_filename
from common import utils, aws_manager
from common.aws_manager import upload_file, dynamo_list, list_videos
from worker import conn
from rq import Queue
from src.main import download_and_process
import logging

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
    results_list = dynamo_list('blur')
    return render_template('index.html', videos=videos, results_list=results_list)


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


@app.route("/requesting", methods=['POST'])
def requesting_video():
    video_name = request.form.get('video')
    blur_is_enabled = request.form.get('blur')
    variance_is_enabled = request.form.get('variance')
    circles_is_enabled = request.form.get('circles')
    if blur_is_enabled or variance_is_enabled or circles_is_enabled:
        # Background process of video processing
        q.enqueue(download_and_process, video_name, blur_is_enabled, variance_is_enabled, circles_is_enabled, BUCKET)
        return render_template("loading.html", video_name=video_name, info='is processing', spin='fa-spin')
    return redirect("/")


@app.route("/download_results", methods=['POST'])
def download_results():
    if request.method == 'POST':
        video_name = request.form.get('video')
        results = str(aws_manager.dynamo_download(video_name))
        return Response(
            results,
            mimetype="text/txt",
            headers={"Content-disposition": "attachment; filename=results.txt"})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
