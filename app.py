import os
from os import path
from flask import Flask, render_template, request, redirect, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
from common import utils
from src.main import main
from worker import conn
from rq import Queue
import time

root = utils.get_project_root()
os.makedirs(os.path.join(str(root), 'data', 'videos'), exist_ok=True)
UPLOAD_FOLDER = os.path.join(str(root), 'data', 'videos')
ALLOWED_EXTENSIONS = {'avi', 'mov', 'flv', 'mp4'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tubus.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
q = Queue(connection=conn, default_timeout=3600)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')
    # if request.method == 'POST':
    #     task_content = request.form['thecontent']
    #     new_task = Todo(content=task_content)
    #
    #     try:
    #         db.session.add(new_task)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return 'There was an issue adding your task'
    # else:
    #     tasks = Todo.query.order_by(Todo.date_created).all()
    #     return render_template('index.html', tasks=tasks)


# @app.route('/buttons', methods=['GET', 'POST'])
# def buttons():
#     if request.method == 'POST':
#         # do stuff when the form is submitted
#
#         # redirect to end the POST handling
#         # the redirect can be to the same route or somewhere else
#         return redirect(url_for('index'))
#
#     # show the form, it wasn't submitted
#     return render_template('buttons.html')


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
#
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'


# Not yet implemented. Video @ 34min
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     flash('update')
#     return 'updated'

def simple_stuff():
    time.sleep(10)
    os.makedirs(os.path.join(str(root), 'data', 'files'), exist_ok=True)
    if os.path.exists(os.path.join(str(root), 'data', 'files')):
        print('files exists')
    else:
        print('there are no files')
    return 'this is simple'


def allowed_video_type(videoname):
    return '.' in videoname and \
           videoname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/data/videos/<videoname>')
# def uploaded_video(videoname):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                videoname)

# def job_stastus(job_id, video_name_no_extension):
#     job = q.fetch_job(job_id)
#     if job is None:
#         return render_template('index.html'), job_status(job_id, video_name_no_extension)
#     if job.is_finished:
#         return video_results(video_name_no_extension)
#     if job.is_failed:
#         response['message'] = job.exc_info.strip().split('\n')[-1]


# def job_status(job_id, video_name_no_extension):
#     job = Job.fetch('video_processing', connection=conn)
#     while True:
#         job.refresh()
#         print(job.get_id(), job.get_status(), job.meta.get('word'))
#         if job.is_finished:
#             print(job.get_status())
#             break
#
#
# def video_results(video_name_no_extension):
#     with open(
#             os.path.join(os.path.join(str(root), 'data', 'files'), video_name_no_extension, 'blur_results.txt'),
#             'r') as result_file:
#         results = result_file.readlines()
#     return render_template('index.html', results=results)


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
            # background_process = q.enqueue(main, job_id='video_processing', result_ttl=5000)
            background_process = q.enqueue(simple_stuff, job_id='video_processing', result_ttl=5000)
            flash('Video is processing')
            job_id = background_process.get_id()
            # # Background process to verify if video processing is completed
            # q.enqueue(job_status, 'video_processing', video_name_no_extension)
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
