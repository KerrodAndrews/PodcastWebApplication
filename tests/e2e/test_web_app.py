import os
from datetime import datetime
import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.abstract_repository import repo_instance
from podcast.authentication.services import auth_services
from podcast import create_app


#Instantiating a testing environment for some of our end-to-end tests (bottom of code).
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "REPOSITORY": 'memory'
    })

    repo_instance = MemoryRepository()
    repo_instance.populate()

    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# End-to-End Testing.
def test_user_registration(client):
    # Simulate registering a new user
    response = client.post('/authentication/register', data={
        'username': 'testuser',
        'password': 'TestPassword123',
        'submit': 'Register'
    })

    # Assert successful registration and redirection
    assert response.status_code == 302  # Check for redirection to homepage
    assert b'Redirecting' in response.data  # Check response contains a redirect message

    login_response = client.post('/authentication/login', data={
        'username': 'testuser',
        'password': 'TestPassword123',
        'submit': 'Login'
    })

    assert login_response.status_code == 302    #Check response status.
    assert b'Redirecting' in login_response.data

def test_search_podcast(client):
    client.post('/authentication/login', data={
        'username': 'testuser',
        'password': 'TestPassword123',
        'submit': 'Login'
    })
    #Example search.
    response = client.get('/search', query_string={
        'query': 'brian denny',
        'parameter': 'Title'
    })

    # Assert the search result page loads successfully and contains the podcast we're looking for.
    assert response.status_code == 200
    assert b'Brian Denny Radio' in response.data

def test_create_playlist_add_podcast_to_playlist(client):
    """Broken since changing how playlists work for A3."""
    client.post('/authentication/login', data={
        'username': 'testuser',
        'password': 'TestPassword123',
        'submit': 'Login'
    })

    #Creating new playlist for the user.
    create_playlist_response = client.post('/playlists/create', data={
        'playlist_name': 'My Favorite Podcasts'
    })

    assert create_playlist_response.status_code == 302  # Redirect.

    #Add a podcast to the playlist
    response = client.post('/playlists/add_podcast/1', data={
        'playlist_id': 1
    })

    assert response.status_code == 302  # Redirect

    #Check podcast is in the playlist
    playlist = repo_instance.get_playlist(1)
    podcast = repo_instance.get_podcast(1)
    assert podcast.title in playlist.get_podcasts()


def test_logout(client):
    client.post('/authentication/login', data={
        'username': 'testuser',
        'password': 'TestPassword123',
        'submit': 'Login'
    })

    # Simulate logging out
    response = client.get('/authentication/logout')

    # Check if the user was logged out and redirected to the homepage
    assert response.status_code == 302
    assert b'Redirecting' in response.data

    # Final check to make sure there is now no logged-in user.
    with client.session_transaction() as session:
        assert session.get('username', '') == ''


def test_review(client):
    """Reviews also had to change how they worked. This no longer executes successfully."""
    client.post('/authentication/login', data={
        'username': 'testuser',
        'password': 'TestPassword123',
        'submit': 'Login'
    })

    response = client.post('/description/1', data={
        'rating': 5,
        'content': 'Amazing podcast! Highly recommend.',
        'submit': 'Submit Review'
    })

    assert response.status_code == 302

    podcast_page = client.get('/description/1')
    assert podcast_page.status_code == 200


    assert b'Amazing podcast! Highly recommend.' in podcast_page.data  # Check the review has been created.
    assert b'5' in podcast_page.data
