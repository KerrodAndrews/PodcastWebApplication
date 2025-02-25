from podcast.adapters.abstract_repository import AbstractRepository
import random

# Case-insensitive search.
def search_string(name: str, substring: str):
    return substring.strip().lower() in name.lower()

def get_random_podcasts(i: int, repo: AbstractRepository):
    podcast_indices = []
    random_podcasts = []
    num_of_podcasts = len(repo.get_podcasts())
    if i > num_of_podcasts:
        raise Exception("Too many podcasts!")

    while len(random_podcasts) < i:
        # Check if index was already, otherwise get another id
        id = random.randint(1, num_of_podcasts - 1)
        if id in podcast_indices:
            continue

        # Attempt adding random_podcasts
        try:
            random_podcasts.append(repo.get_podcast(id))
        except StopIteration as e:
            print("Could not find podcast ID! Re-scanning with a different ID.")
        except Exception as e:
            print(e)
        else:
            podcast_indices.append(id)

    """podcast_indices = []
    for j in range(i):
        podcast_indices.append(random.randint(0, num_of_podcasts - 1))
    for n in podcast_indices:
        random_podcasts.append(repo.get_podcast(n))"""
    return random_podcasts
