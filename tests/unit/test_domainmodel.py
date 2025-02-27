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

    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, "Joe Toste Podcast - Sales Training Expert", my_author)


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


@pytest.fixture
def my_episode():
    test_1_datetime = datetime(2024, 8, 6, 10, 0, 0)
    test_1_date, test_1_time = test_1_datetime.date(), test_1_datetime.time()
    return Episode(1, 10, "Pilot Episode", "abcd", 1250, "Our first podcast episode", test_1_date, test_1_time)

@pytest.fixture
def my_memory_repository():
    test_repo = MemoryRepository()
    return test_repo

@pytest.fixture
def wacky_podcast(my_author):
    #  Podcast with a stupid category to test repository adding new categories correctly
    wacky_podcast = Podcast(101, "Joe Toste Podcast - Sales Training Expert")
    wacky_podcast.add_category(Category(666, "Satan worship!"))
    return wacky_podcast

def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2,"My First Podcast", author1)
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"
    podcast4 = Podcast(123, "a_podcast")
    assert podcast4.title is 'a_podcast'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"
    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100,"Joe Toste Podcast - Sales Training Expert", author1)
    podcast2 = Podcast(200, "Voices in AI", author2)
    podcast3 = Podcast(101, "Law Talk", author3)
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, "Joe Toste Podcast - Sales Training Expert", author1)
    podcast2 = Podcast(100, "Voices in AI", author2)
    podcast3 = Podcast(101, "Law Talk", author3)
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, "Joe Toste Podcast - Sales Training Expert", author1)
    podcast2 = Podcast(100, "Voices in AI", author2)
    podcast3 = Podcast(101, "Law Talk", author3)
    assert podcast1 == podcast2
    assert podcast2 < podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"
    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, "Voices in AI", author2)
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

#  : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes


# unit tests for episode class


def test_episode_initialization(my_episode):
    test_1_datetime = datetime(2024, 8, 6, 10, 0, 0)
    test_1_date, test_1_time = test_1_datetime.date(), test_1_datetime.time()
    assert my_episode.title == "Pilot Episode"
    assert my_episode.publish_time == test_1_time
    assert my_episode.publish_date == test_1_date
    assert my_episode.id == 1
    assert my_episode.podcast_id == 10
    assert my_episode.description == "Our first podcast episode"


def test_episode_eq():
    test_1_datetime = datetime(2024, 8, 6, 10, 0, 0)
    test_1_date = test_1_datetime.date()
    test_1_time = test_1_datetime.time()
    episode1 = Episode(1, 10, "Pilot Episode", "abcd.co.nz", 1250, "Our first podcast episode", test_1_date, test_1_time)
    episode2 = Episode(1, 14, "The Beginning", "abcd.com", 1221, "Opening", test_1_date, test_1_time)
    episode3 = Episode(2, 11, "Pilot Episode", "abcd.co.au", 1533, "Wowee let's go!", test_1_date, test_1_time)

    assert episode1 == episode1
    assert episode1 != episode2
    assert episode1 != episode3


def test_episode_hash():
    test_1_date = datetime(2024, 8, 6)
    test_1_time = datetime(2024, 8, 6, 10, 0, 0)
    episode1 = Episode(1, 10, "Pilot Episode", "abcd", 1250, "Our first podcast episode", test_1_date, test_1_time)
    episode2 = Episode(1, 10, "Pilot Episode", "abcd", 1250, "Our first podcast episode", test_1_date, test_1_time)
    episode3 = Episode(3, 12, "Pilot Episode", "abcd", 1300, "Our first podcast episode", test_1_date, test_1_time)
    episode_set = set()
    episode_set.add(episode1)
    episode_set.add(episode2)
    episode_set.add(episode3)
    assert len(episode_set) == 2   #Since both have the same episode and podcast id.


def test_episode_lt():
    test_1_date = datetime(2024, 8, 6)
    test_1_time = datetime(2024, 8, 6, 10, 0, 0)
    episode1 = Episode(1, 10, "Pilot Episode", "abcd", 1250, "Our first podcast episode", test_1_date, test_1_time)
    episode2 = Episode(2, 10, "Second Episode", "abcd123", 1275, "Our second podcast episode", test_1_date, test_1_time)
    episode3 = Episode(3, 12, "Pilot Episode", "abcd456", 1300, "I'm a different podcast!", test_1_date, test_1_time)
    assert episode1 < episode2
    assert episode1 < episode3


# unit tests for review class


def test_review_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    review1 = Review(1, user1, 8, "This podcast is very good", 1)
    review2 = Review(2, user2, 9, "This podcast is very good", 2)
    review3 = Review(3, user3, 2, "This podcast is very bad", 3)
    assert repr(review1) == "<User: shyamli \nRating: 8><Content: This podcast is very good \nReview ID: 1><Episode ID: None \nPodcast ID: 1>"
    assert repr(review2) == "<User: asma \nRating: 9><Content: This podcast is very good \nReview ID: 2><Episode ID: None \nPodcast ID: 2>"
    assert repr(review3) == "<User: jenny \nRating: 2><Content: This podcast is very bad \nReview ID: 3><Episode ID: None \nPodcast ID: 3>"
    assert review2.rating == 9
    assert review1.episode_id is None
    assert review1.podcast_id is 1


def test_review_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(3, "JeNNy  ", "pw87465")
    review1 = Review(1, user1, 8, "This podcast is very good", 4)
    review2 = Review(1, user1, 8, "This podcast is very good", 4)
    review3 = Review(3, user2, 2, "This podcast is very bad", 4)

    assert review1 == review2
    assert review1 != review3


def test_review_hash():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(3, "JeNNy  ", "pw87465")
    review1 = Review(1, user1, 8, "This podcast is very good", 4)
    review2 = Review(1, user1, 8, "This podcast is very good", 3)
    review3 = Review(3, user2, 2, "This podcast is very bad", 2)
    review_set = set()
    review_set.add(review1)
    review_set.add(review2)
    review_set.add(review3)
    assert len(review_set) == 2


def test_review_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    review1 = Review(1, user1, 8, "This podcast is very good", 1)
    review2 = Review(2, user2, 9, "This podcast is very good", 2)
    review3 = Review(3, user3, 2, "This podcast is very bad", 3)
    assert review1 < review2
    assert review2 < review3
    assert review3 > review1
    review_list = [review3, review2, review1]
    assert sorted(review_list) == [review1, review2, review3]


# unit test for Playlist class


def test_playlist_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    playlist1 = Playlist(1, "My playlist", user1)

    assert playlist1.playlist_id == 1
    assert playlist1.user.username == "shyamli"
    assert playlist1.playlist_name == "My playlist"


def test_playlist_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    playlist1 = Playlist(1, "My playlist", user1)
    playlist2 = Playlist(1, "My playlist", user1)
    playlist3 = Playlist(3, "Jenny's playlist", user3)
    assert playlist1 == playlist2
    assert playlist1 != playlist3


def test_playlist_hash():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    playlist1 = Playlist(1, "My playlist", user1)
    playlist2 = Playlist(1, "My playlist", user1)
    playlist3 = Playlist(3, "Jenny's playlist", user2)
    playlist_set = set()
    playlist_set.add(playlist1)
    playlist_set.add(playlist2)
    playlist_set.add(playlist3)

    assert len(playlist_set) == 2


def test_playlist_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    playlist1 = Playlist(1, "A playlist", user1)
    playlist2 = Playlist(2, "B playlist", user2)
    playlist3 = Playlist(3, "C playlist", user3)
    assert playlist1 < playlist2
    assert playlist2 < playlist3
    assert playlist3 > playlist1


def test_playlist_add_remove_playlists(my_user):
    test_1_date = datetime(2024, 8, 6)
    test_1_time = datetime(2024, 8, 6, 10, 0, 0)
    my_episode = Episode(1, 10, "Pilot Episode", "abcd", 1250, "Our first podcast episode", test_1_date, test_1_time)
    new_playlist = Playlist(1, "Test Playlist", my_user)
    new_playlist.playlist_add(my_episode)
    assert len(new_playlist.playlist) == 1
    new_playlist.playlist_remove(my_episode)
    assert len(new_playlist.playlist) == 0


# Unit tests for CSVDataReader.

def test_CSVDataReader_init():
    datareader = CSVDataReader()
    assert isinstance(datareader.get_podcasts(), list)
    assert isinstance(datareader.get_episodes(), list)
    assert os.path.exists(datareader.podcasts_filepath)
    assert os.path.exists(datareader.episodes_filepath)

def test_CSVDataReader_load_podcast_data():
    datareader = CSVDataReader()
    datareader.load_podcast_data()
    assert len(datareader.get_podcasts()) > 0

def test_CSVDataReader_load_episode_data():
    datareader = CSVDataReader()
    datareader.load_episode_data()
    assert len(datareader.get_episodes()) > 0

def test_CSVDataReader_get_podcasts():
    datareader = CSVDataReader()
    podcasts = datareader.get_podcasts()
    assert isinstance(podcasts, list)
    assert len(podcasts) > 0

def test_CSVDataReader_get_episodes():
    datareader = CSVDataReader()
    episodes = datareader.get_episodes()
    assert isinstance(episodes, list)
    assert len(episodes) > 0

# Unit tests for memory repository.


def test_add_author(my_memory_repository, my_author):
    my_memory_repository.add_author(my_author)
    assert my_memory_repository.get_author(1) == my_author
    assert my_memory_repository.get_author("Joe Toste") == my_author


def test_add_podcast(my_memory_repository, my_podcast):
    my_memory_repository.add_podcast(my_podcast)
    assert my_memory_repository.get_podcast(100) == my_podcast
    assert my_memory_repository.get_podcast("Joe Toste Podcast - Sales Training Expert") == my_podcast


def test_add_category(my_memory_repository, my_podcast):
    category = Category(1, "Sales")
    my_podcast.add_category(category)
    my_memory_repository.add_podcast(my_podcast)
    assert my_memory_repository.get_category(1) == category
    assert my_memory_repository.get_category("Sales") == category


def test_get_podcasts_by_name(my_memory_repository, my_podcast):
    my_memory_repository.add_podcast(my_podcast)
    sorted_podcasts = my_memory_repository.get_podcasts_by_name()
    assert sorted_podcasts[0].title == "Joe Toste Podcast - Sales Training Expert"


def test_get_podcasts_by_language(my_memory_repository, my_podcast):
    my_podcast.language = "English"
    my_memory_repository.add_podcast(my_podcast)
    sorted_podcasts = my_memory_repository.get_podcasts_by_language()
    assert sorted_podcasts[0].language == "English"


def test_random_podcast_selection(my_podcast):
    repo_instance.add_podcast(my_podcast)
    random_podcasts = repo_instance.get_random_podcasts(num_of_podcasts=1)
    assert len(random_podcasts) == 1


def test_get_authors(my_memory_repository, my_author):
    my_memory_repository.add_author(my_author)
    authors = my_memory_repository.get_authors()
    assert my_author in authors


def test_add_new_category_from_podcast(my_memory_repository, wacky_podcast):
    my_memory_repository.add_podcast(wacky_podcast)
    assert my_memory_repository.get_category(666).name == "Satan worship!"


def test_author_not_found(my_memory_repository):
    with pytest.raises(StopIteration):
        my_memory_repository.get_author(999)


def test_podcast_not_found(my_memory_repository):
    with pytest.raises(StopIteration):
        my_memory_repository.get_podcast(999)


def test_category_not_found(my_memory_repository):
    with pytest.raises(StopIteration):
        my_memory_repository.get_category(999)

# Unit tests for authentication services.


def test_register_user_get_user():
    auth_services.register_user("abc", "abcdEfg123", repo_instance)
    auth_services.register_user("Agent Smith", "01001000 01101001 World", repo_instance)
    auth_services.register_user("abc", "01001000 01101001 World", repo_instance)

    user_1 = auth_services.get_user("abc", repo_instance)
    user_2 = auth_services.get_user("agent smith", repo_instance)
    # User 3 cannot register with the same username as User 1
    assert user_1.id == 1
    assert user_2.id == 2
    assert user_1.username == "abc"
    assert user_2.username == "agent smith"
    assert user_1.password == "abcdEfg123"
    assert user_2.password == "01001000 01101001 World"

def test_user_registered():
    assert auth_services.user_registered("atk", repo_instance) is False
    auth_services.register_user("atk", "abcdEfg123", repo_instance)
    assert auth_services.user_registered("atk", repo_instance) is True

def test_authenticate_user():
    assert auth_services.authenticate_user("luck", "abcdEfg123", repo_instance) is False
    auth_services.register_user("luck", "abcdEfg123", repo_instance)
    assert auth_services.authenticate_user("luck", "NotSoLuckyBruteForce", repo_instance) is False
    assert auth_services.authenticate_user("luck", "abcdEfg123", repo_instance) is True
