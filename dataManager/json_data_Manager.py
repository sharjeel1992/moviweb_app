import requests

from moviweb_app.dataManager.data_manager_interface import DataManagerInterface
import json


class JSONDataManager(DataManagerInterface):
    API = 'http://www.omdbapi.com/?apikey=c61fc86&t='

    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def get_all_users(self):
        try:
            with open(self.filename, "r") as fileobj:
                data = json.load(fileobj)
                self.data = data
                return data
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {str(e)}")
            return None

    def get_user_movies(self, user_id):
        if self.data is None:
            raise ValueError("No data available. Load data before accessing user movies.")
        for name in self.data:
            if name['id'] == user_id:
                return name["movies"]

    def add_user(self, name):
        if not self.data:
            new_id = 1
        else:
            new_id = max(user['id'] for user in self.data) + 1
        new_user = {
            "name": name,
            "id": new_id,
            "movies": []
        }
        self.data.append(new_user)
        with open(self.filename, "w") as update_file:
            json.dump(self.data, update_file, indent=4)
        return self.data

    def add_movie(self, movies, movie_name):
        fetch_data = requests.get(self.API + movie_name)
        access_data = fetch_data.json()
        if 'Error' in access_data:
            error_message = access_data['Error']
            raise ValueError(f"Error retrieving movie information: {error_message}")
        if not movies:
            new_id = 1
        else:
            new_id = max(movie['id'] for movie in movies) + 1
        new_movie = {
            "id": new_id,
            "name": movie_name,
            "director": access_data["Director"],
            "year": access_data["Year"],
            "rating": access_data["imdbRating"]
        }
        movies.append(new_movie)
        with open(self.filename, "w") as update_file:
            json.dump(self.data, update_file, indent=4)
        return movies

    def get_movie(self, user_id, movie_id):
        movies = self.get_user_movies(user_id)
        for movie in movies:
            if movie['id'] == movie_id:
                movie['user_id'] = user_id
                return movie

    def update_movie(self, user_id, movie_id, movie_name, director, year, rating):
        movies = self.get_user_movies(user_id)
        for movie in movies:
            if movie['id'] == movie_id:
                movie['name'] = movie_name
                movie['director'] = director
                movie['year'] = year
                movie['rating'] = rating
                break
        with open(self.filename, 'w') as update_file:
            json.dump(self.data, update_file, indent=4)

    def delete_movie(self, movies, movie_id):
        for movie in movies:
            if movie['id'] == movie_id:
                movies.remove(movie)
        with open(self.filename, "w") as update_file:
            json.dump(self.data, update_file, indent=4)
        return self.data
