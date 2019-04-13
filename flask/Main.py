from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def main():
    title =  "Plane Captures"
    return render_template("index.html", title=title)

@app.route('/refresh')
def refresh():
    # search for videos in a directory
    # list all videos
    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True) # , host="0.0.0.0")
