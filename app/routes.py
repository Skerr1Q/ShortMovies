from flask import render_template, url_for, flash, redirect, session, request, jsonify
from app import app, db
from app.forms import LoginForm, RegForm, MovieForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Role, UserRoles, Movie
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from flask_user import roles_required
import time
#route for main page
@app.route('/')
@app.route('/index')
def index():
	page = request.args.get('page', 1, type=int)
	movies = Movie.query.order_by(Movie.timestamp.desc()).paginate(
		page, 3, False)	
	next_url = url_for('index', page=movies.next_num) \
		if movies.has_next else None
	prev_url = url_for('index', page=movies.prev_num) \
		if movies.has_prev else None

	return render_template('index.html', title="Main Page", movies=movies.items, next_url=next_url, prev_url=prev_url)
#routes for login and logout

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
	  	user = User.query.filter_by(email=form.email.data).first()
	  	if user is None or not user.check_password(form.password.data):
	  		flash('Invalid email or password')
	  		return redirect(url_for('login'))
  		login_user(user, remember=form.remember_me.data)
  		next_page = request.args.get('next')
  		if not next_page or url_parse(next_page).netloc != '':
  			next_page = url_for('index')
  			return redirect(next_page)
  		return redirect(url_for('index'))
	return render_template('login.html',title="Login", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
#sign up 
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('sign_up.html', title='Register', form=form)
#add movie 
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
	form = MovieForm()
	if form.validate_on_submit():
		movie = Movie(name=form.name.data, link=form.link.data, description=form.description.data, poster=form.poster.data)
		db.session.add(movie)
		db.session.commit()
		return redirect('index')
	return render_template('add_movie.html',title="Add movie", form = form)
#get custom movie page
@app.route('/movie/<name>', methods=['GET', 'POST'])
def get_movie(name):
  movie = Movie.query.filter_by(name = name).first_or_404()
  return render_template('movie_p.html',title=movie, movie=movie)
#jsonify dict with movie data
@app.route('/api/movie/<name>', methods=['GET', 'POST'])
def get_user(name):
  movie = Movie.query.filter_by(name = name).first_or_404()
  return jsonify(movie.to_dict())
#search route
@app.route("/search")
def search():
	return render_template('search.html',title="Search movie", reload = time.time())
#admin
@roles_required('admin')
@app.route('/admin')
def admin():
	if not current_user.has_role("admin"):
		return redirect(url_for('index'))