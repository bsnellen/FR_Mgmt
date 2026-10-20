import mariadb
import sys
from flask import Flask, render_template

import config

app = Flask(__name__)


def get_db_connection():
    try:
        conn = mariadb.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}", file=sys.stderr)
        return None


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
