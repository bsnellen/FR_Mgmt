from flask import Flask, render_template, request, redirect, url_for
from db import get_radcheck_users, update_radcheck_user, delete_radcheck_user

app = Flask(__name__)


@app.route("/")
def index():
    users = get_radcheck_users()
    return render_template("index.html", users=users)


@app.route("/update", methods=["POST"])
def update():
    username = request.form.get("username")
    attribute = request.form.get("attribute")
    op = request.form.get("op")
    value = request.form.get("value")
    old_username = request.form.get("old_username")
    old_attribute = request.form.get("old_attribute")
    if username and attribute and op and value:
        update_radcheck_user(username, attribute, op, value, old_username, old_attribute)
    return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete():
    username = request.form.get("username")
    attribute = request.form.get("attribute")
    if username and attribute:
        delete_radcheck_user(username, attribute)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
