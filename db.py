import mariadb
import sys
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def get_db_connection():
    """Connect to existing MariaDB server."""
    try:
        conn = mariadb.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}", file=sys.stderr)
        return None


def get_radcheck_users():
    """Fetch all users from the radius radcheck table."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM radcheck")
        users = [row[0] for row in cursor.fetchall()]
        return users
    except mariadb.Error as e:
        print(f"Error fetching users: {e}", file=sys.stderr)
        return []
    finally:
        if conn:
            conn.close()
