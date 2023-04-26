from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('aa.html')

@app.route("/getimage")
def get_img():
    return "/static/img/2.jpg"


if __name__ == '__main__':
    app.run(debug=True)
