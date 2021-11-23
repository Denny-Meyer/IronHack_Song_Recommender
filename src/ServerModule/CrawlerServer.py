from flask import Flask, render_template
from flask.globals import request
from werkzeug.utils import redirect



class application():
    
    app = Flask(__name__)
    
    @app.route('/', methods=['GET','POST'])
    def index():
        if request.method == 'POST':
            if request.form['next_page'] == 'next':
                print('directing to next page')
                return redirect('crawler')
        return render_template('index.html')


    @app.route('/crawler', methods=['GET','POST'])
    def crawler():
        if request.method == 'POST':
            if request.form['btn'] == 'prev':
                return redirect('/')
            else:
                s_text = request.form['btn']
            print('searching for song', s_text)
        return render_template('search.html')

    def run(self):
        self.app.run()
