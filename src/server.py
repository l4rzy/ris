from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug import secure_filename
import os
from timeit import default_timer as timer

class Server:
    def __init__(self, engine):
        print("initializing server")
        self.engine = engine
        self.host = '0.0.0.0'
        self.port = '8001'
        self.debug = True

        self.UPLOAD_FOLDER = './uploads'
        self.ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def run(self, method):
        app = Flask(__name__)
        app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER

        @app.route('/get/<path:subpath>', methods=['GET'])
        def givefile(subpath):
            return send_from_directory('/', subpath)

        @app.route('/', methods=['GET', 'POST'])
        def homepage():
            if request.method == 'POST':
                f = request.files['file']
                path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
                f.save(path)
                print(f"Saved file f{path}")
                start = timer()

                ret = self.engine.look(path, method)
                end = timer()
                sec = end-start
                print(f"Took {sec} second(s) to complete")
                return render_template('home.html', results = ret, sec=sec)

            return render_template('home.html', results = [], sec=0)

        app.run(host=self.host, port=self.port, debug=self.debug, use_reloader=False)

