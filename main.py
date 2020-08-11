from flask import Flask
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy

from wtforms import StringField, SubmitField, validators

from markupsafe import escape
from flask import url_for, request, session, make_response
from flask import redirect, abort, render_template, flash
from datetime import datetime

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "hard to guess string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)
  def __repr__(self):
    return '<Role %r>' % self.name 
  users = db.relationship('User', backref='role')

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  def __repr__(self):
    return '<User %r>' % self.username
  rold_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
  return render_template('index.html')

class NameForm(FlaskForm):
  name = StringField('What is your name?', [validators.DataRequired()])
  submit = SubmitField('Submit')

@app.route('/survey', methods=['GET','POST'])
def survey():
  form=NameForm()
  if form.validate_on_submit():
    old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
      flash('Looks like you have changed your name!')
    session['name'] = form.name.data
    form.name.data=''
    return redirect(url_for('survey'))
  return render_template('survey.html', form=form, name=session.get('name'))

@app.route('/user/<username>')
def show_user_profile(username):
    return render_template('user.html', username=username)

@app.route('/time')
def time():
  return render_template('time.html', current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
  return render_template('/errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('/errors/500.html'), 500

if __name__=='__main__':
  # manager.run()
  app.run(debug = True, host ='0.0.0.0', port = 8080)