from provider import *

from flask import Flask, jsonify, redirect, url_for, render_template, request
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    init()
    image = "hello"
    if request.method=="POST":
        image = request.form['img']
        return render_template("home.html", imgRes = validate(image))
    return render_template("home.html")
    

if __name__ == '__main__':
    app.run(debug=True)