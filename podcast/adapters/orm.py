from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey, Text, Date, Time, MetaData
)
from sqlalchemy.orm import registry, relationship

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

metadata = MetaData()
mapper_registry = registry()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

podcast_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True)
)

# Episodes should have links to its podcast through its foreign keys
episode_table = Table(
    'episodes', mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_url', Text, nullable=True),
    Column('audio_len', Integer, nullable=True),
    Column('description', String(255), nullable=True),
    Column('pub_date', Date, nullable=True),
    Column('pub_time', Time, nullable=True)
)

categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64), nullable=False)
)

# Resolve many-to-many relationship between podcast and categories
podcast_categories_table = Table(
    'podcast_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id'))
)

users_table = Table(
    'users', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', Text, nullable=False),
    Column('password', Text, nullable=False)
)


reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('rating', Integer),
    Column('content', Text)
)

playlist_table = Table(
    'playlists', mapper_registry.metadata,
    Column('playlist_id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_name', String(255), nullable=False),
    Column('user_id', ForeignKey('users.id')),  # Foreign key to the User table
)

# Associative table for Playlist
playlist_episodes_table = Table(
    'playlist_episodes', mapper_registry.metadata,
    Column('playlist_id', ForeignKey('playlists.playlist_id'), primary_key=True),
    Column('episode_id', ForeignKey('episodes.episode_id'), primary_key=True)
)

# Associative table for Playlist
playlist_podcasts_table = Table(
    'playlist_podcasts', mapper_registry.metadata,
    Column('playlist_id', ForeignKey('playlists.playlist_id'), primary_key=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id'), primary_key=True)
)


def map_model_to_tables():
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.name,
    })

    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.category_id,
        '_name': categories_table.c.category_name,
    })

    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.title,
        '_image': podcast_table.c.image_url,
        '_description': podcast_table.c.description,
        '_language': podcast_table.c.language,
        '_website': podcast_table.c.website_url,
        '_itunes_id': podcast_table.c.itunes_id,
        '_author': relationship(Author),
        'categories': relationship(Category, secondary=podcast_categories_table),
        'episodes': relationship(Episode, back_populates='_podcast', cascade='all, delete-orphan')
    })

    mapper_registry.map_imperatively(Episode, episode_table, properties={
        '_episode_id': episode_table.c.episode_id,
        '_podcast_id': episode_table.c.podcast_id,
        '_title': episode_table.c.title,
        '_audio': episode_table.c.audio_url,
        '_audio_len': episode_table.c.audio_len,
        '_description': episode_table.c.description,
        '_publish_date': episode_table.c.pub_date,
        '_publish_time': episode_table.c.pub_time,
        '_podcast': relationship(Podcast, back_populates='episodes')
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.id,
        '_username': users_table.c.username,
        '_password': users_table.c.password,
    })

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_review_id': reviews_table.c.id,
        '_user': relationship(User, backref='reviews'),
        #'_podcast_id': relationship(Podcast, backref='reviews'),
        '_podcast_id': reviews_table.c.podcast_id,
        '_rating': reviews_table.c.rating,
        '_content': reviews_table.c.content
    })

    mapper_registry.map_imperatively(Playlist, playlist_table, properties={
        '_playlist_id': playlist_table.c.playlist_id,
        '_playlist_name': playlist_table.c.playlist_name,
        '_user': relationship(User, backref='playlists'),
        '_episodes': relationship(Episode, secondary=playlist_episodes_table),
        '_podcasts': relationship(Podcast, secondary=playlist_podcasts_table)
    })
