from os import environ

import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from AddForm import AddForm
from UpdateForm import UpdateForm

MOVIES_DB_URL = 'https://api.themoviedb.org/3/search/movie'
API_KEY = environ.get('API_KEY')
HEADERS = {"accept": "application/json"}

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-collection.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100), nullable=False)


db.create_all()


@app.route("/")
def home():
    movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i
    db.session.commit()
    return render_template("index.html", movies=movies)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = UpdateForm()
    movie_id = request.args.get('movie_id')
    movie_to_update = db.session.get(entity=Movie, ident=movie_id)
    if form.validate_on_submit():
        movie_to_update.rating = form.new_rating.data
        movie_to_update.review = form.new_review.data
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', form=form, movie=movie_to_update)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    movie_id = request.args.get('movie_id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        response = requests.get(MOVIES_DB_URL,
                                headers=HEADERS,
                                params={
                                    'api_key': API_KEY,
                                    'query': form.title.data
                                })
        movies = response.json()['results']
        return render_template('select.html', movies=movies)
    return render_template('add.html', form=form)


@app.route('/select', methods=['GET', 'POST'])
def select():
    movie_id = request.args.get('movie_id')
    response = requests.get(url=f'https://api.themoviedb.org/3/movie/{movie_id}',
                            headers=HEADERS,
                            params={
                                'api_key': API_KEY
                            })
    movie_info = response.json()
    movie_to_add = Movie(
        id=movie_info['id'],
        title=movie_info['title'],
        year=movie_info['release_date'][0:4],
        description=movie_info['overview'],
        rating=round(movie_info['vote_average'], 1),
        ranking='',
        review='',
        img_url=f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}"
    )
    db.session.add(movie_to_add)
    db.session.commit()

    return redirect(url_for('edit', movie_id=movie_to_add.id))


if __name__ == '__main__':
    app.run(debug=True)
