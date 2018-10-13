from flask import Flask, render_template
app = Flask(__name__)

@app.route("/<int:comic_id>")
def comic(comic_id):
    return render_template('comic.html')

@app.route("/")
def hello():
    maxid = 100 # TODO: query storage to get max comic ID
    return comic(maxid)
