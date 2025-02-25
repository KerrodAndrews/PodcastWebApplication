from __future__ import annotations
from typing import List
from datetime import datetime


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self.id}: {self._name}>"

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, title: str, author: Author = "No Author Listed", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []
        self.reviews = []  # list for reviews

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @author.setter
    def author(self, author: Author):
        if isinstance(author, Author):
            self._author = author
        else:
            self._author = None

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @itunes_id.setter
    def itunes_id(self, value):
        self._itunes_id = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    def get_pleasant_categories(self):
        if hasattr(self, 'categories'):  # Memory version
            return " | ".join([category.name for category in self.categories])
        else:  # Database version
            return " | ".join([category._name for category in self._categories])

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __str__(self) -> str:
        return f"{self._name}"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = []
        self._playlists = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def __repr__(self):
        return f"<User {self._id}: {self._username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:
    def __init__(self, episode_id: int, podcast_id: int, title: str, audio: str, audio_len: int,
                 description: str, publish_date: datetime.date, publish_time: datetime.time):
        validate_non_negative_int(episode_id)
        self._episode_id = episode_id
        self._podcast_id = podcast_id
        self._title = title
        self._audio = audio
        self._audio_len = audio_len
        self._description = description

        # datetime.date(yr, month, day) and datetime.date(hr, min, sec) to initialize these
        self._publish_date = publish_date
        self._publish_time = publish_time

    @property
    def id(self) -> int:
        return self._episode_id

    @property
    def podcast_id(self) -> int:
        return self._podcast_id

    @podcast_id.setter
    def podcast_id(self, new_podcast: int):
        self._podcast_id = new_podcast

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title)
        self._title = new_title

    @property
    def audio(self) -> str:
        return self._audio

    @audio.setter
    def audio(self, new_audio: str):
        if not isinstance(new_audio, str):
            raise TypeError("Audio must be a string object.")
        self._audio = new_audio

    @property
    def audio_len(self) -> int:
        return self._audio_len

    @audio_len.setter
    def audio_len(self, new_audio_len: int):
        validate_non_negative_int(new_audio_len)
        self._audio_len = new_audio_len

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        validate_non_empty_string(new_description)
        self._description = new_description

    @property
    def publish_date(self) -> datetime:
        return self._publish_date

    @publish_date.setter
    def publish_date(self, new_publish_date: datetime):
        if not isinstance(new_publish_date, datetime):
            raise TypeError("Publish_date must be a datetime object.")
        self._publish_date = new_publish_date

    @property
    def publish_time(self) -> datetime:
        return self._publish_time

    @publish_time.setter
    def publish_time(self, new_publish_time: datetime):
        if not isinstance(new_publish_time, datetime):
            raise TypeError("Publish_date must be a datetime object.")
        self._publish_time = new_publish_time

    def __repr__(self):
        return (f"<Title: {self.title} \nDescription: {self.description}" +
                f"\nPublish Date: {self.publish_date} \nPublish Time: {self.publish_time}" +
                f"\nEpisode ID: {self._episode_id} \nPodcast ID: {self._podcast_id}" +
                f"\nAudio Link: {self._audio} \nAudio Len: {self._audio_len}>")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Episode):
            return False
        return (self._episode_id == other.id) and (self.podcast_id == other.podcast_id)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Episode):
            raise TypeError("Episode must be an episode object.")
        if self._podcast_id < other.podcast_id:
            return True
        elif self._podcast_id == other.podcast_id:
            if self._episode_id < other.id:
                return True
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.id, self.title))

    def episode_id(self):
        return self._episode_id


class Review:
    def __init__(self, review_id: int, user: User, rating: int, content: str, podcast_id: int):
        # if not isinstance(user, User):
        # raise TypeError("User must be a User object.")
        if rating < 0 or rating > 10:
            raise ValueError("Rating must be between 0 and 10.")
        self._review_id = review_id
        self._user = user
        self._rating = rating
        self._content = content
        self._episode_id = None
        self._podcast_id = podcast_id

    @property
    def review_id(self) -> int:
        return self._review_id

    @review_id.setter
    def review_id(self, new_id: int):
        if not isinstance(new_id, int):
            raise TypeError("Review_id must be a Integer object.")
        self._review_id = new_id

    @property
    def episode_id(self):
        return self._episode_id

    @episode_id.setter
    def episode_id(self, new_episode_id: int):
        # Resets podcast id when setting episode id, can only have one or the other.
        self._podcast_id = None
        self._episode_id = new_episode_id

    @property
    def podcast_id(self):
        return self._podcast_id

    @podcast_id.setter
    def podcast_id(self, new_podcast_id: int):
        # Resets episode id when setting podcast id.
        self._episode_id = None
        self._podcast_id = new_podcast_id

    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, new_user: User):
        if not isinstance(new_user, User):
            raise TypeError("User must be a User object.")
        self._user = new_user

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, new_rating: int):
        validate_non_negative_int(new_rating)
        self._rating = new_rating

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, new_content: str):
        validate_non_empty_string(new_content)
        self._content = new_content

    def __repr__(self) -> str:
        string_representation = (f"<User: {self._user.username} \nRating: {self._rating}>" +
                                 f"<Content: {self._content} \nReview ID: {self._review_id}>" +
                                 f"<Episode ID: {self._episode_id} \nPodcast ID: {self._podcast_id}>")
        return string_representation

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return self._review_id == other.review_id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return self._review_id < other.review_id

    def __hash__(self) -> int:
        return hash(self.review_id)


class Playlist:
    # Initialize with no episodes, add after object creation.
    def __init__(self, playlist_id: int, playlist_name: str, user: User):
        # if not isinstance(user, User):
        # raise TypeError("Owner must be a User object.")
        self._playlist_id = playlist_id
        self._playlist_name = playlist_name
        #self._playlist = []
        self._user = user
        self._podcasts = []
        self._episodes = []

    @property
    def playlist(self) -> List[Episode]:
        return self._episodes

    def playlist_add(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Must be a Episode object.")
        self._episodes.append(episode)

    def playlist_remove(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Must be a Episode object.")
        if episode in self._episodes:
            self._episodes.remove(episode)
        #index = 0
        #while index < len(self._playlist):
            #if self._playlist[index] == episode:
                #del self._playlist[index]
            #index += 1

    @property
    def playlist_id(self) -> int:
        return self._playlist_id

    @property
    def playlist_name(self) -> str:
        return self._playlist_name

    @playlist_name.setter
    def playlist_name(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError("Playlist_name must be a String object.")
        self._playlist_name = new_name

    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, new_user: User):
        if not isinstance(new_user, User):
            raise TypeError("Owner must be a User object.")
        self._user = new_user

    def __repr__(self):
        string_representation = (f"<Playlist Name: {self._playlist_name} \nOwner as user: {self._user.username}>" +
                                 f"<\nPlaylist ID: {self._playlist_id}>")

        # Adds every string representation of each episode into string representation of playlist
        for episode in self._episodes:
            string_representation += f"\nEpisode: {episode}"

        return string_representation

    def __eq__(self, other) -> bool:
        if not isinstance(other, Playlist):
            return False
        return self._playlist_id == other._playlist_id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Playlist):
            raise TypeError("Must be a playlist!")
        return self._playlist_name < other._playlist_name

    def __hash__(self) -> int:
        return hash(self.playlist_id)

    def add_podcast(self, podcast : Podcast):
        self._podcasts.append(podcast)

    def remove_podcast(self, podcast : Podcast):
        if podcast in self._podcasts:
            self._podcasts.remove(podcast)

    def get_podcasts(self):
        return self._podcasts

    def get_episodes(self):
        return self._episodes

    def remove_episode(self, episode : Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)
