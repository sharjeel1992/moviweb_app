from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """this function is an abstract function for getting all users from the database"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """This function is abstract function to get list of movies based on user's id"""
        pass

    @abstractmethod
    def add_user(self, name):
        """This function will enforce the name parameter to fetch data from API"""
        pass

    @abstractmethod
    def add_movie(self, movies, movie_name):
        """This method will be used to add movies"""
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, movie_name, director, year, rating):
        """This method will force above-mentioned arguments to be implemented to update the movie"""
        pass

    @abstractmethod
    def delete_movie(self, movies, movie_id):
        """This method will enforce the delete function"""
        pass
