from flask import Flask, render_template, redirect
from flask_login import login_required, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired
import os
from users import users
from resources import yaml_function, thread_update, load_api_data


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ThisisMySecret!'

login = LoginManager(app)

class LoginForm(FlaskForm):
    myTemplates = [(x.split('.j2')[0], x.split('.j2')[0])  for x in os.listdir('./configTemplates')]
    username = StringField('username', validators=[InputRequired('You need a username')])
    password = PasswordField('password', validators=[InputRequired('Fill in the password!')])
    myConfig = TextAreaField('myConfig')
    templates = SelectField('templates', choices=myTemplates)

class MainLoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('You need a username')])
    password = PasswordField('password', validators=[InputRequired('Fill in the password!')])

users = {'anthony': 'a123', 'hana': 'h123'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Instantiate the form
    form = MainLoginForm()
    if form.validate_on_submit():
        if form.username.data in users.keys():
            user.authenticated = True
            return redirect(url_for("form"))
    return render_template('login.html', form=form)

#POST required to submit the user/password

@app.route("/entries")
def entries():
    loaded_data = yaml_function('my_devices.yml', 'load')
    return render_template("results.html", entries=loaded_data)

@app.route('/form', methods=['GET', 'POST'])
def form():
    #Instantiate the form
    form = LoginForm()
    print(type(form))
    if form.validate_on_submit():
        return render_template('results.html', username=form.username.data, password=form.password.data, myConfig=form.myConfig.data, templates=form.templates.data)
    #Add the form to the page
    return render_template('form.html', form=form)

if __name__ == "__main__":
    thread_update()
    app.run(debug=True)
