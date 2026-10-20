from flask import Flask, render_template
from db import get_radcheck_users

app = Flask(__name__)


@app.route("/")
def index():
    users = get_radcheck_users()
    return render_template("index.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
