
from flask import Flask, render_template, request, url_for, redirect
from dataManager.json_data_Manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('dataManager/data.json')


@app.route('/')
def home():
    """
    This is a static home page route that will render the homepage.html
    """
    return render_template('homepage.html')


@app.route('/users')
def list_users():
    """
    This function uses data manager to ger the list of users and render to the users html
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    This function uses data manager function to get movies from the database based on user id passed to it
    and renders the movie template
    """
    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    This function is handles get and post requests.Get is to render add user template and
    post is when user enters its name and press enter.it will get that name and pass to data manger function
    that will add user to the database
    """
    if request.method == 'POST':
        name = request.form.get('name')
        data_manager.add_user(name)
        return redirect(url_for('list_users'))
    else:
        return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=["POST", "GET"])
def add_movie(user_id):
    """
    This route is for adding movie based on user id.
    Get is to render add movie template, and
    post is when a user enters movie name,data manager function will do necessary actions
    with post-method it will redirect its user movies page
    """
    if request.method == 'POST':
        movies = data_manager.get_user_movies(user_id)
        movie_name = request.form.get('name')
        data_manager.add_movie(movies, movie_name)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
      This route will render a form with get request and will fetch details and pass it on
      to data manger function that will do necessary actions and redirects it to user movies page
    """
    if request.method == 'POST':
        movie_name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')
        data_manager.update_movie(user_id, movie_id, movie_name, director, year, rating)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        movie = data_manager.get_movie(user_id, movie_id)
        return render_template('update_movie.html', movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
      This route will get user id and movie id and the function will pass arguments to
      the data manager function that will delete the movie from databases
    """
    movies = data_manager.get_user_movies(user_id)
    data_manager.delete_movie(movies, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """This route is for to handle page not found error"""
    return render_template(f'404.html {e}'), 404


if __name__ == '__main__':
    app.run(debug=True)
