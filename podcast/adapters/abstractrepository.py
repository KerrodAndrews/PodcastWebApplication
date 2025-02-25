import abc
import os
repo_instance = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_author(self, author):
        """adds author to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self):
        """returns list of authors."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_podcast(self, podcast):
        """adds podcast to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts(self):
        """returns list of podcasts."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self):
        """returns list of categories."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_info):
        """returns podcast based on either id or name."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, author_info):
        """returns author based on either id or name."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_category(self, category_info):
        """returns category based on either id or name."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_name(self):
        """returns the lists of podcasts, sorted alphabetically."""
        raise NotImplementedError

    @abc.abstractmethod
    def populate(self):
        """fills the repository with information from a briefly instantiated CSVDataReader object."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        """adds user to the memory or database repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        """Returns a registered user with the username, if it exists."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_users(self):
        """Returns a list of registered users."""
        raise NotImplementedError

    @abc.abstractmethod
    def save_review(self, review):
        """Save a review."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_playlist(self, playlist):
        """Add a new playlist."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist(self, playlist_id: int):
        """Retrieve a playlist by its ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlists_by_user(self, user):
        """Retrieve playlists associated with a specific user."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_playlist_id(self) -> int:
        """Generate the next playlist ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def save_playlist(self, playlist):
        """Save or update a playlist."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_for_podcast(self, podcast_id: int):
        """Takes a podcastid as an int, and returns all episodes for that podcast as a list."""
        raise NotImplementedError
