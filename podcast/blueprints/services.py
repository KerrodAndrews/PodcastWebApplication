import podcast.adapters.abstract_repository as repo
from podcast.domainmodel.model import *


def add_playlist(playlist: Playlist):
    repo.repo_instance.add_playlist(playlist)

def get_episode_by_title(title):
    return repo.repo_instance.get_episode_by_title(title)

def get_episodes_for_podcast(podcast: Podcast):
    return repo.repo_instance.get_episodes_for_podcast(podcast)

def get_length():
    return repo.repo_instance.get_length()

def get_next_playlist_id():
    return repo.repo_instance.get_next_playlist_id()

def get_playlist(playlist_id: int):
    return repo.repo_instance.get_playlist(playlist_id)

def get_playlists_by_user(user: User):
    return repo.repo_instance.get_playlists_by_user(user)

def get_podcast_by_title(podcast_title: str):
    return repo.repo_instance.get_podcast_by_title(podcast_title)

def get_podcast(podcast_id: int):
    return repo.repo_instance.get_podcast(podcast_id)

def get_podcasts_by_name():
    return repo.repo_instance.get_podcasts_by_name()

def get_repo():
    return repo.repo_instance

def get_review(podcast_id: int):
    return repo.repo_instance.get_review(podcast_id)

def get_user(username: str):
    return repo.repo_instance.get_user(username)

def get_users():
    return repo.repo_instance.get_users()

def remove_episode():
    repo.repo_instance.remove_episode()

def save_playlist(playlist: Playlist):
    repo.repo_instance.save_playlist(playlist)

def save_review(review: Review):
    repo.repo_instance.save_review(review)
