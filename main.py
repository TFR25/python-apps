from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from datetime import datetime


app = Flask(__name__)
Bootstrap5(app)

now = datetime.now()
current_year = now.year


@app.route("/")
def home():
    return render_template('index.html', year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
