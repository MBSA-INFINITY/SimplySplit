from flask import Flask, session, redirect, render_template, request, abort
from controllers.user import insert_user
from controllers.dashboard import add_new_friend, add_new_group, get_friends_list, get_group_list, get_group_members, get_group_name
from controllers.group import split_expense

app = Flask(__name__)
app.secret_key="mbsaiaditya"

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

@app.route("/")
def start():
    if session.get("user_id") is None:
        return redirect("/login")
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    if session.get("user_id") is not None:
        session.pop("user_id")
        return redirect("/")
    return "LoggedIn"

@app.route("/login", methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_details = dict(request.form)
        user_id = insert_user(user_details)
        session["user_id"] = user_id
        return redirect("/")
    if session.get("user_id") is not None:
        return redirect("/")
    return render_template("login.html")


@app.route("/dashboard", methods=['GET','POST'])
@login_is_required
def dashboard():
    user_id = session.get("user_id")
    friends_list = get_friends_list(user_id)
    groups_list = get_group_list(user_id)
    return render_template("dashboard.html", user_id=user_id, friends_list=friends_list, groups_list=groups_list)

@app.route("/add-friend", methods=['POST'])
def add_friend():
    user_id = session.get("user_id")
    form_data = dict(request.form)
    friend_user_id = form_data.get("friend_user_id")
    add_new_friend(user_id, friend_user_id)
    return redirect("/dashboard")

@app.route("/add-group", methods=['POST'])
def add_group():
    user_id = session.get("user_id")
    form_data = dict(request.form)
    user_list = form_data.get("user_list")
    group_name = form_data.get("group_name")
    user_list = user_list.split(",")
    add_new_group(user_id, user_list, group_name)
    return redirect("/dashboard")

@app.route("/group/<string:group_id>", methods=['GET','POST'])
def get_group_details(group_id):
    user_id = session.get("user_id")
    group_members = get_group_members(group_id, user_id)
    group_name = get_group_name(group_id)
    return render_template("group.html", user_id=user_id,group_id=group_id, group_members=group_members,group_name=group_name )

@app.route("/add-transaction/<string:group_id>", methods=['POST'])
def add_group_transaction(group_id):
    if request.method == 'POST':
        user_id = session.get("user_id")
        form_data = dict(request.form)
        members_involved = request.form.getlist("people_involved")
        split_expense(group_id, form_data, members_involved, user_id)
        return redirect(f"/group/{group_id}")
    # user_id = session.get("user_id")
    # group_members = get_group_members(group_id, user_id)
    # group_name = get_group_name(group_id)
    # return render_template("group.html", user_id=user_id,group_id=group_id, group_members=group_members,group_name=group_name )




if __name__ == '__main__':
    app.run(debug=True)