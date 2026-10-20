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
    """Fetch all users from the radius radcheck table with their group memberships."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, attribute, op, value FROM radcheck")
        users = {}
        for row in cursor.fetchall():
            username = row[0]
            if username not in users:
                users[username] = {"username": username, "checks": [], "groups": []}
            users[username]["checks"].append({"attribute": row[1], "op": row[2], "value": row[3]})
        
        cursor.execute("SELECT username, groupname, priority FROM radusergroup")
        for row in cursor.fetchall():
            username = row[0]
            if username in users:
                users[username]["groups"].append({"groupname": row[1], "priority": row[2]})
        
        return list(users.values())
    except mariadb.Error as e:
        print(f"Error fetching users: {e}", file=sys.stderr)
        return []
    finally:
        if conn:
            conn.close()


def update_radcheck_user(username, attribute, op, value, old_username=None, old_attribute=None):
    """Update or insert a user entry in radcheck table."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        if old_username and old_attribute:
            cursor.execute(
                "UPDATE radcheck SET username = ?, attribute = ?, op = ?, value = ? "
                "WHERE username = ? AND attribute = ?",
                (username, attribute, op, value, old_username, old_attribute)
            )
        else:
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


def get_radusergroup_memberships(username):
    """Fetch group memberships for a specific user from radusergroup table."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT groupname, priority FROM radusergroup WHERE username = ?", (username,))
        groups = [{"groupname": row[0], "priority": row[1]} for row in cursor.fetchall()]
        return groups
    except mariadb.Error as e:
        print(f"Error fetching group memberships: {e}", file=sys.stderr)
        return []
    finally:
        if conn:
            conn.close()


def add_radusergroup_membership(username, groupname, priority=0):
    """Add a group membership for a user in radusergroup table."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO radusergroup (username, groupname, priority) VALUES (?, ?, ?)",
            (username, groupname, priority)
        )
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Error adding group membership: {e}", file=sys.stderr)
        return False
    finally:
        if conn:
            conn.close()


def delete_radusergroup_membership(username, groupname):
    """Delete a group membership for a user from radusergroup table."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM radusergroup WHERE username = ? AND groupname = ?", (username, groupname))
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Error deleting group membership: {e}", file=sys.stderr)
        return False
    finally:
        if conn:
            conn.close()
