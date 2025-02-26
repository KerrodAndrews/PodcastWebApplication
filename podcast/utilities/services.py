from podcast.adapters.memory_repository import MemoryRepository
from podcast.domainmodel.model import Podcast



def get_all_podcasts(repo: MemoryRepository):
    return repo.get_podcasts()


def get_podcast_by_id(podcast_id: int, repo: MemoryRepository):
    return repo.get_podcast(podcast_id)


def get_all_authors(repo: MemoryRepository):
    return repo.get_authors()


def get_all_categories(repo: MemoryRepository):
    return repo.get_categories()


def add_podcast(podcast: Podcast, repo: MemoryRepository):
    repo.add_podcast(podcast)


def search_by_podcast_name(search: str, repo: MemoryRepository):
    return [podcast for podcast in repo.get_podcasts() if search.lower() in podcast.title.lower()]


def search_by_author_name(search: str, repo: MemoryRepository):
    return [podcast for podcast in repo.get_podcasts() if search.lower() in podcast.author.name.lower()]


def search_by_category(search: str, repo: MemoryRepository):
    possible_categories = [category for category in repo.get_categories() if search.lower() in category.name.lower()]
    found_podcasts = []
    for cat in possible_categories:
        for podcast in cat.get_podcasts():
            if podcast not in found_podcasts:
                found_podcasts.append(podcast)
    return found_podcasts
