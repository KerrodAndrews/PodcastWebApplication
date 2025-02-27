from datetime import date, datetime

import pytest

from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import User, Podcast, Category, Review


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_podcast_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_podcasts = repo.get_number_of_podcasts()

    # Check that the query returned the expected number of podcasts.
    assert number_of_podcasts == 100  # Assuming 100 podcasts as a placeholder

def test_repository_can_add_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_podcasts = repo.get_number_of_podcasts()

    new_podcast_id = number_of_podcasts + 1

    podcast = Podcast(
        new_podcast_id,
        'Tech Talks',
        description='A podcast about technology',
        language='English',
        website='https://techtalks.com'
    )
    repo.add_podcast(podcast)

    assert repo.get_podcast(new_podcast_id) == podcast

def test_repository_can_retrieve_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast(1)

    # Check that the Podcast has the expected title.
    assert podcast.title == 'Tech Talks'

def test_repository_does_not_retrieve_a_non_existent_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast(999)
    assert podcast is None


def test_repository_can_retrieve_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    categories = repo.get_categories()

    assert len(categories) == 5  # Assuming 5 categories for this test

    category_one = [category for category in categories if category.name == 'Technology'][0]
    category_two = [category for category in categories if category.name == 'Business'][0]

    assert category_one.name == 'Technology'
    assert category_two.name == 'Business'

def test_repository_can_get_first_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast(0)
    assert podcast.title == 'Tech Talks'

def test_repository_can_get_last_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast(len(repo.get_podcasts()))
    assert podcast.title == 'Science Weekly'

def test_repository_can_get_podcasts_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcasts = repo.get_podcasts_by_id([2, 5, 6])

    assert len(podcasts) == 3
    assert podcasts[0].title == 'Tech Talks'
    assert podcasts[1].title == "Startup Stories"
    assert podcasts[2].title == 'Science Weekly'

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcasts = [repo.get_podcast(0)]

    assert len(podcasts) == 0

def test_repository_can_add_a_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    category = Category('Health')
    repo.add_category(category)

    assert category in repo.get_categories()

def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    podcast = repo.get_podcast(2)
    review = Review(5, user, 10, 'Great podcast, site needs some work...', 2)

    repo.save_review(review)

    assert review == repo.get_review(5)

def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast(2)
    user = repo.get_user('thorke')
    review = Review(1, user, 10, 'Great podcast!')


def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews()) == 5  # Example number of reviews in the database

def test_can_retrieve_a_podcast_and_add_a_review_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch Podcast and User.
    podcast = repo.get_podcast(5)
    user = repo.get_user('thorke')

    # Create a new Review, connecting it to the Podcast and User.
    review = Review(1, user, 10, 'Great podcast!')
    repo.save_review(review)

    podcast_fetched = repo.get_podcast(5)
    user_fetched = repo.get_user('thorke')

    assert review in podcast_fetched.reviews
