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
        cursor.execute("SELECT username, attribute, op, value FROM radcheck")
        users = [{"username": row[0], "attribute": row[1], "op": row[2], "value": row[3]} for row in cursor.fetchall()]
        return users
    except mariadb.Error as e:
        print(f"Error fetching users: {e}", file=sys.stderr)
        return []
    finally:
        if conn:
            conn.close()


def update_radcheck_user(username, attribute, op, value):
    """Update or insert a user entry in radcheck table."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO radcheck (username, attribute, op, value) VALUES (?, ?, ?, ?) "
            "ON DUPLICATE KEY UPDATE attribute = ?, op = ?, value = ?",
            (username, attribute, op, value, attribute, op, value)
        )
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Error updating user: {e}", file=sys.stderr)
        return False
    finally:
        if conn:
            conn.close()


def delete_radcheck_user(username, attribute):
    """Delete a user entry from radcheck table."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM radcheck WHERE username = ? AND attribute = ?", (username, attribute))
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Error deleting user: {e}", file=sys.stderr)
        return False
    finally:
        if conn:
            conn.close()
