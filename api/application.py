# Setting flask
from flask import Flask, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

# The last thing that you will need is to config you database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Now let's define our db
db = SQLAlchemy(app)

# This will only work if you import SQLAlchemy since you need to define db
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, unique=True, nullable=False)

    # Where it will show your "data"
    def __repr__(self):
        return f"{self.name} - {self.genre} - {self.year}"

# Setting primary route
@app.route('/')
def index():
    return 'Hello. Go to route: /movies Or try accessing an specific movie by going to route: /movies/The movie id that you want to access'

# Setting another route, which will show the movies
@app.route('/movies')
def get_movies():
    movies = Movie.query.all()

    output = []
    for movie in movies:
        # "Collecting the movie data to output it"
        movie_data = {'name': movie.name, 'genre': movie.genre, 'year': movie.year}
        # Output the movie data
        output.append(movie_data)

    return {"movies": output}

# Now, I'm going to create a new route that will allow me to see each movie individualy only saying its id
@app.route('/movies/<id>')
def get_movie(id):
    # Find movie or throw a not found error
    movie = Movie.query.get_or_404(id)
    # Calling a jsonfy (can also do this if does not want to work with dictionary)
    return ({"name": movie.name, "genre": movie.genre, "year": movie.year})


# Let's create a route that will post new movies
@app.route('/movies', methods=['POST'])
def add_movie():
    # to use request you need to import request from flask
    movie = Movie(name=request.json['name'], genre=request.json['genre'], year=request.json['year'])
    db.session.add(movie)
    db.session.commit()
    return {'id': movie.id}
# You can use portman to make this post request the right url is http://127.0.0.1:5000/movies


# Now Let's create a route that will allow me to delete old movies
@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    # get the movie id
    movie = Movie.query.get(id)

    # But before deleting it check if it is not "Null"
    if movie is None:
        return {"error": "Not Found"}

    # Well since it is not null remove it
    db.session.delete(movie)
    db.session.commit()
    return{"message": "Movie with id: " + str(id) + " DELETED!!!"}
