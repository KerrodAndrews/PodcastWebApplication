from abc import ABC
from typing import List, Type

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from podcast.adapters.abstract_repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.utils import search_string
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # Podcast
    def get_podcasts(self, sorting: bool = False) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts

    def get_podcasts_by_name(self):
        podcasts = self._session_cm.session.query(Podcast).all()
        return sorted(podcasts)

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(
                Podcast._id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print(f'Podcast {podcast_id} was not found')
        return podcast

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.add(podcast)
            scm.commit()

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        with self._session_cm as scm:
            for podcast in podcasts:
                scm.session.add(podcast)
            scm.commit()

    def get_number_of_podcasts(self) -> int:
        num_podcasts = self._session_cm.session.query(Podcast).count()
        return num_podcasts

    def get_podcast_by_title(self, title: str) -> Podcast:
        """Retrieve a Podcast by its title."""
        title_part = title.split("' by ")[0]
        podcast_title = title_part.split(": '")[1].strip()
        return self._session_cm.session.query(Podcast).filter(Podcast._title == podcast_title).first()

    # Author

    def get_author(self, author_info):
        # Maintained polymorphic lookup capabilities.
        try:
            if isinstance(author_info, str):
                query = self._session_cm.session.query(Author).filter(Author._name == author_info)
                author = query.one()
            elif isinstance(author_info, int):
                query = self._session_cm.session.query(Author).filter(Author._id == author_info)
                author = query.one()
            else:
                raise TypeError("Unsupported search parameter.")
            return author
        except NoResultFound:
            print(f'Author {author_info} was not found.')

    def get_authors(self) -> List[Author]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    if author.name is None:
                        raise ValueError("Author name cannot be None")

                    existing_author = scm.session.query(Author).filter_by(_name=author.name).first()
                    if not existing_author:
                        # Only add the author if they don't exist in the database
                        scm.session.add(author)
            scm.commit()

    def get_number_of_authors(self) -> int:
        num_authors = self._session_cm.session.query(Author).count()
        return num_authors

    # Category

    def get_category(self, category_info):
        try:
            if isinstance(category_info, int):
                query = self._session_cm.session.query(Category).filter(Category._id == category_info)
                category = query.one()
            elif isinstance(category_info, str):
                query = self._session_cm.session.query(Category).filter(Category._name == category_info)
                category = query.one()
            else:
                raise TypeError("Unsupported search parameter.")
            return category
        except NoResultFound:
            print(f'Category {category_info} was not found.')
    def get_categories(self) -> list[Type[Category]]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    def add_category(self, category: Category):
        with self._session_cm as scm:
            scm.session.add(category)
            scm.commit()

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()

    # Episode
    def get_episodes(self, sorting: bool = False) -> list[Type[Episode]]:
        pass

    def get_episode(self, episode_id: int) -> Episode:
        pass

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.add(episode)
            scm.commit()

    def add_multiple_episodes(self, episodes: List[Episode]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for episode in episodes:
                    scm.session.add(episode)
            scm.commit()

    def get_number_of_episodes(self):
        pass

    def get_episodes_for_podcast(self, podcast_id: int) -> List[Episode]:
        """Get all episodes for a specific podcast by podcast_id."""
        with self._session_cm as scm:
            episodes = scm.session.query(Episode).filter(
                Episode._podcast_id == podcast_id
            ).all()
            return episodes

    def get_number_of_episodes_for_podcast(self, podcast_id: int) -> int:
        """ Returns the number of episodes for a particular podcast by podcast_id. """
        pass

    def get_episode_by_title(self, title: str) -> Episode:
        title_part = title.split("' by ")[0]
        episode_title = title_part.split(": '")[1].strip()
        return self._session_cm.session.query(Episode).filter(Episode._title == episode_title).first()

    # User

    def add_user(self, user: User):
        with self._session_cm as scm:
            if not user.username:
                raise ValueError("User username cannot be Empty!")
            existing_user = scm.session.query(User).filter_by(_username=user.username).first()
            if not existing_user:
                try:
                    scm.session.add(user)
                    scm.commit()
                except Exception as e:
                    scm.rollback()
                    print(f"Error adding user {user.username}: {e}")

    def get_user(self, username: str) -> User | None:
        user = None
        try:
            query = self._session_cm.session.query(User).filter(
                User._username == username.lower()) ## problem?!
            user = query.one()
        except NoResultFound:
            print(f'User {username} was not found.')
        return user

    def get_users(self) -> List[User]:
        """Retrieves all users from the database."""
        with self._session_cm as scm:
            users = scm.session.query(User).all()
        return users

    # Reviews

    def save_review(self, review):
        """Save a review to the database."""
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_review(self, podcast_id):
        with self._session_cm as scm:
            reviews = scm.session.query(Review).filter(Review._podcast_id == podcast_id).all()
        return reviews

    def get_length(self):
        with self._session_cm as scm:
            reviews = scm.session.query(Review).all()
        return len(reviews)

    # Playlists:

    def add_playlist(self, playlist):
        """Add a playlist to the database."""
        with self._session_cm as scm:
            scm.session.add(playlist)
            scm.commit()

    def get_playlist(self, playlist_id: int) -> Playlist:
        """Retrieve a playlist by its ID."""
        playlist = self._session_cm.session.query(Playlist).filter(Playlist._playlist_id == playlist_id).first()
        return playlist

    def get_playlists_by_user(self, user: User) -> List[Playlist]:
        """Retrieve playlists associated with a specific user."""
        playlists = self._session_cm.session.query(Playlist).filter(Playlist._user == user).all()
        return playlists

    def get_next_playlist_id(self) -> int:
        """Generate the next playlist ID based on the current max ID in the database."""
        max_id = self._session_cm.session.query(func.max(Playlist._playlist_id)).scalar()
        return (max_id or 0) + 1

    def save_playlist(self, playlist):
        """Save or update a playlist in the database."""
        with self._session_cm as scm:
            existing_playlist = scm.session.query(Playlist).filter(Playlist.playlist_id == playlist.playlist_id).first()
            if existing_playlist:
                scm.session.merge(playlist)  # Update existing playlist
            else:
                scm.session.add(playlist)  # Add new playlist
            scm.commit()

    def get_episode_by_title(self, title: str) -> Episode:
        """Retrieve an episode by its title."""
        return self._session_cm.session.query(Episode).filter(Episode._title == title).first()

    # Searches

    def search_podcasts_by_name(self, title_string: str) -> List[Podcast]:
        """Retrieve podcasts whose title contains the title_string passed by the user."""
        search_term = f"%{search_string(title_string)}%"
        podcasts = self._session_cm.session.query(Podcast).filter(
            func.lower(Podcast._title).like(func.lower(search_term))
        ).all()
        return podcasts

    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        search_term = f"%{search_string(author_name)}%"
        podcasts = self._session_cm.session.query(Podcast).join(Author).filter(
            func.lower(Author._name).like(func.lower(search_term))
        ).all()
        return podcasts

    def search_podcast_by_category(self, category_string: str) -> List[Podcast]:
        search_term = f"%{search_string(category_string)}%"
        podcasts = self._session_cm.session.query(Podcast).join(Category, Podcast._categories).filter(
            func.lower(Category._name).like(func.lower(search_term))
        ).all()
        return podcasts

    def search_podcasts_by_language(self, language_string: str) -> List[Podcast]:
        pass

    # Populate
    def populate(self):
        reader = CSVDataReader()

        authors = reader.get_authors()
        podcasts = reader.get_podcasts()
        categories = reader.get_categories()
        episodes = reader.get_episodes()

        # Add authors to the repo
        self.add_multiple_authors(authors)

        # Add categories to the repo
        self.add_multiple_categories(categories)
        # Add podcasts to the repo
        self.add_multiple_podcasts(podcasts)

        # Add episodes to the repo
        self.add_multiple_episodes(episodes)
