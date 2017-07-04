from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)
from werkzeug import secure_filename
import os

class Result:
    def __init__(self, path, similarity):
        self.url = url_for('img_static', filename=path)
        self.similarity = similarity

    def serialize(self):
        return render_template("result.html", url=self.url, similarity=self.similarity)
    
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)


app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    elif endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@app.route('/img/<path:filename>')
def img_static(filename):
    return send_from_directory(app.root_path + '/fake_results/', filename)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def uploadfile():
    if request.method == 'POST':
        similarity_wanted = request.form['similarity_wanted']
        files = request.files['file_source']
        if files and allowed_file(files.filename):
            filename_source = secure_filename(files.filename)
            app.logger.info('FileName: ' + filename_source)
            updir = os.path.join(basedir, 'upload/')
            files.save(os.path.join(updir, filename_source))
            file_size = os.path.getsize(os.path.join(updir, filename_source))

            #results = get_results()
            results = []
            
            #os.remove(os.path.join(updir, filename_source))
            return jsonify(name=filename_source, size=file_size, results=[e.serialize() for e in results])

def get_results():
    fake_results = []
    for filename in os.listdir(os.path.join(basedir, "fake_results/")):
        fake_results.append(Result(filename, 1))
    return fake_results


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
