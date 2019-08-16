from flask import Flask, render_template, redirect, url_for, flash, session, abort
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired
import os
from users import users
import gc
from resources import yaml_function, thread_update


app = Flask(__name__)

app.config["SECRET_KEY"] = "ThisisMySecret!"


class TemplateForm(FlaskForm):
    myTemplates = [
        (x.split(".j2")[0], x.split(".j2")[0]) for x in os.listdir("./configTemplates")
    ]
    hostname = StringField(
        "hostname", validators=[InputRequired("You need a hostname")]
    )
    myConfig = TextAreaField("myConfig")
    templates = SelectField("templates", choices=myTemplates)


class MainLoginForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired("You need a username")]
    )
    password = PasswordField(
        "password", validators=[InputRequired("Fill in the password!")]
    )


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("login"))

    return wrap


@app.route("/")
def base_uri():
    return redirect(url_for("login"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = MainLoginForm()
    usernames = [user for user in users.keys()]
    if form.validate_on_submit():
        if (
            form.username.data not in usernames
            or users[form.username.data] != form.password.data
        ):
            flash("Username/password incorrect!")
            return redirect(url_for("login"))
        else:
            session["logged_in"] = True
            session["username"] = form.username.data
            flash("Successfully logged in!")
            return redirect(url_for("entries"))
    return render_template("login.html", form=form)


# POST required to submit the user/password


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for("login"))


@app.route("/entries/")
@login_required
def entries():
    try:
        loaded_data = yaml_function("my_devices.yml", "load")
    except FileNotFoundError:
        return abort(404)
    return render_template("entries.html", entries=loaded_data)


@app.route("/templates/", methods=["GET", "POST"])
@login_required
def templates():
    # Instantiate the form
    form = TemplateForm()
    if form.validate_on_submit():
        return render_template(
            "entries.html",
            hostname=form.hostname.data,
            myConfig=form.myConfig.data,
            templates=form.templates.data,
        )
    # Add the form to the page
    return render_template("form.html", form=form)


if __name__ == "__main__":
    # thread_update()
    app.run(debug=True, host="0.0.0.0")


"""A super simple API endpoint"""
# @app.route('/devices/<string:getsomethingcool>/')
# def get_something_cool(getsomethingcool: str):
#    return "Your string is {}".format(getsomethingcool)

"""Blueprint placeholder for when a
   Blueprint is needed"""

# def main():
# register_blueprints()
# app.run(debug=True)

# def register_blueprints():
# from views import common
# app.register_blueprint(common.blueprint)
