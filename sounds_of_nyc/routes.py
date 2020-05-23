from sounds_of_nyc import sounds_of_nyc
from flask import render_template, request

@sounds_of_nyc.route('/')
def index():
    return render_template("index.html")

@sounds_of_nyc.route('/', methods=['POST'])
def index_post():
    text = request.form['link']
    return text

@sounds_of_nyc.route('/res')
def search_res(search):
    res = [search]
    return res
    #display something
