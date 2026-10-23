from flask import Flask, render_template, request, redirect, url_for
from db import (
    get_radcheck_users, update_radcheck_user, delete_radcheck_user,
    add_radusergroup_membership, delete_radusergroup_membership,
    get_groups, get_group, update_group_attribute, delete_group_attribute, delete_group,
    create_opnsense_dhcp_reservation, delete_opnsense_dhcp_reservation, get_group_vlan_number
)

app = Flask(__name__)


@app.route("/")
def index():
    users = get_radcheck_users()
    groups = get_groups()
    return render_template("index.html", users=users, groups=groups)


@app.route("/update", methods=["POST"])
def update():
    username = request.form.get("username")
    attribute = request.form.get("attribute")
    op = request.form.get("op")
    value = request.form.get("value")
    description = request.form.get("description", "")
    old_username = request.form.get("old_username")
    old_attribute = request.form.get("old_attribute")
    if username and attribute and op and value:
        update_radcheck_user(username, attribute, op, value, old_username, old_attribute, description)
    return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete():
    username = request.form.get("username")
    attribute = request.form.get("attribute")
    if username and attribute:
        delete_radcheck_user(username, attribute)
    return redirect(url_for("index"))


@app.route("/add_group", methods=["POST"])
def add_group():
    username = request.form.get("username")
    groupname = request.form.get("groupname")
    priority = int(request.form.get("priority", 0))
    if username and groupname:
        add_radusergroup_membership(username, groupname, priority)
    return redirect(url_for("index"))


@app.route("/delete_group", methods=["POST"])
def delete_group():
    username = request.form.get("username")
    groupname = request.form.get("groupname")
    if username and groupname:
        delete_radusergroup_membership(username, groupname)
    return redirect(url_for("index"))


@app.route("/groups")
def groups():
    groups = get_groups()
    return render_template("groups.html", groups=groups)


@app.route("/groups/create", methods=["POST"])
def create_group():
    groupname = request.form.get("groupname")
    attribute = request.form.get("attribute")
    op = request.form.get("op")
    value = request.form.get("value")
    if groupname and attribute and op and value:
        update_group_attribute(groupname, attribute, op, value)
    return redirect(url_for("groups"))


@app.route("/groups/update", methods=["POST"])
def update_group():
    groupname = request.form.get("groupname")
    attribute = request.form.get("attribute")
    op = request.form.get("op")
    value = request.form.get("value")
    old_groupname = request.form.get("old_groupname")
    old_attribute = request.form.get("old_attribute")
    if groupname and attribute and op and value:
        update_group_attribute(groupname, attribute, op, value, old_attribute)
    return redirect(url_for("groups"))


@app.route("/groups/add_attr", methods=["POST"])
def add_group_attr():
    groupname = request.form.get("groupname")
    attribute = request.form.get("attribute")
    op = request.form.get("op")
    value = request.form.get("value")
    if groupname and attribute and op and value:
        update_group_attribute(groupname, attribute, op, value)
    return redirect(url_for("groups"))


@app.route("/groups/delete_attr", methods=["POST"])
def delete_group_attr():
    groupname = request.form.get("groupname")
    attribute = request.form.get("attribute")
    if groupname and attribute:
        delete_group_attribute(groupname, attribute)
    return redirect(url_for("groups"))


@app.route("/groups/delete", methods=["POST"])
def delete_group_entry():
    groupname = request.form.get("groupname")
    if groupname:
        delete_group(groupname)
    return redirect(url_for("groups"))


@app.route("/add_dhcp_reservation", methods=["POST"])
def add_dhcp_reservation():
    username = request.form.get("username")
    ip_address = request.form.get("ip_address")
    hostname = request.form.get("hostname", "")
    groupname = request.form.get("groupname", "")
    
    if username and ip_address:
        vlan_number = None
        if groupname:
            vlan_number = get_group_vlan_number(groupname)
        
        if vlan_number is not None:
            ip_parts = ip_address.split('.')
            if len(ip_parts) == 4:
                ip_parts[2] = str(vlan_number)
                ip_address = '.'.join(ip_parts)
        
        create_opnsense_dhcp_reservation(username, ip_address, hostname)
    return redirect(url_for("index"))


@app.route("/delete_dhcp_reservation", methods=["POST"])
def delete_dhcp_reservation():
    username = request.form.get("username")
    if username:
        delete_opnsense_dhcp_reservation(username)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
