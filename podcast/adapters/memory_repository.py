import podcast
from podcast.adapters.abstract_repository import AbstractRepository
from podcast.domainmodel.model import *
from podcast.adapters.datareader.csvdatareader import CSVDataReader
import random

"""
The updated Memory Repository is now responsible for initializing domain model objects, rather than simply
retrieving them from the CSVDataReader, as it was doing before. There is the possibility the conversion function
is supposed to be defined in the services.py file, but this can be something to revisit if we have leftover time.
"""


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__podcasts = list()
        self.__authors = list()
        self.__categories = list()
        self.__users = list()
        self.__reviews = list()
        self.__playlists = list()
        self.__episodes = list()
        self.__playlist_count = 1

    def get_author(self, author_info):
        """
        I have made the retrieval functions polymorphic to simplify use and support lookup via either
        name or id number.
        """
        if isinstance(author_info, int):
            return next(author for author in self.__authors if author.id == author_info)
        elif isinstance(author_info, str):
            return next(author for author in self.__authors if author.name == author_info)
        else:
            raise TypeError("Unsupported search parameter.")

    def get_podcast(self, podcast_info):
        if isinstance(podcast_info, int):
            return next(pod for pod in self.__podcasts if pod.id == podcast_info)
        elif isinstance(podcast_info, str):
            return next(pod for pod in self.__podcasts if pod.title == podcast_info)
        else:
            raise TypeError("Unsupported search parameter.")

    def get_category(self, category_info):
        if isinstance(category_info, int):
            return next(category for category in self.__categories if category.id == category_info)
        elif isinstance(category_info, str):
            return next(category for category in self.__categories if category.name == category_info)
        else:
            raise TypeError("Unsupported search parameter.")

    def get_user(self, username):
        registered_user = None
        for user in self.__users:
            if user.username == username:
                registered_user = user
                break
        if registered_user is None:
            return None
        else:
            return registered_user

    def get_authors(self):
        return self.__authors

    def get_podcasts(self):
        return self.__podcasts

    def get_categories(self):
        return self.__categories

    def get_users(self):
        return self.__users

    def add_author(self, author: Author):
        self.__authors.append(author)

    def add_podcast(self, podcast: Podcast):
        self.__podcasts.append(podcast)
        for cat in podcast.categories:
            if cat not in self.get_categories():
                self.add_category(cat)

    def add_category(self, category: Category):
        self.__categories.append(category)

    def add_user(self, user: User):
        self.__users.append(user)

    def add_episode(self, episode: Episode):
        self.__episodes.append(episode)

    def get_podcasts_by_name(self):
        return sorted(self.__podcasts, key=lambda x: x.title)

    def get_podcasts_by_language(self):
        """Didn't end up using this in final version. Will probably change when implementing different search criteria
        for podcasts. Better to have and not need though."""
        return sorted(self.__podcasts, key=lambda x: x.language)

    def populate(self):
        reader = CSVDataReader()

        authors = reader.get_authors()
        podcasts = reader.get_podcasts()
        categories = reader.get_categories()
        episodes = reader.get_episodes()

        # Add authors to the repo
        for auth in authors:
            self.add_author(auth)

        # Add categories to the repo
        for cat in categories:
            self.add_category(cat)

        # Add podcasts to the repo
        for pod in podcasts:
            self.add_podcast(pod)

        # Add episodes to the repo
        for ep in episodes:
            self.add_episode(ep)

    def save_review(self, review):
        self.__reviews.append(review)

    def add_playlist(self, playlist):
        self.__playlists.append(playlist)

    def get_playlist(self, playlist_id: int):
        for playlist in self.__playlists:
            if playlist.playlist_id == playlist_id:
                return playlist
        return None

    def get_playlists_by_user(self, user: User):
        return [playlist for playlist in self.__playlists if playlist.user == user]

    def get_next_playlist_id(self):
        next_id = self.__playlist_count
        self.__playlist_count += 1
        return next_id

    def save_playlist(self, playlist):
        for index, existing_playlist in enumerate(self.__playlists):
            if existing_playlist.playlist_id == playlist.playlist_id:
                self.__playlists[index] = playlist
                return
        self.add_playlist(playlist)

    def get_episodes_for_podcast(self, podcast_id: int):
        podcast = self.get_podcast(podcast_id)
        return podcast.episodes
        #return [ep for ep in self.__episodes if ep.podcast_id == podcast_id]

    def get_podcast_by_title(self, title : str):
        title_part = title.split("' by ")[0]
        podcast_title = title_part.split(": '")[1].strip()
        for pod in self.__podcasts:
            if pod.title == podcast_title:
                return pod

    def get_episode_by_title(self, title : str):
        for episode in self.__episodes:
            if episode.title == title:
                return episode

    def get_review(self, podcast_id):
        return [review for review in self.__reviews if review.podcast_id == podcast_id]

    def get_length(self):
        return len(self.__reviews)
