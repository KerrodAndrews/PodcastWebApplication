import pytest
import datetime
from sqlalchemy.exc import IntegrityError
from podcast.domainmodel.model import User, Podcast, Author, Review, Category

# Example date for test cases
podcast_date = datetime.date(2023, 5, 20)


def insert_user(empty_session, values=None):
    new_username = "Andrew"
    new_password = "1234"

    if values is not None:
        new_username = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_username, 'password': new_password})
    row = empty_session.execute('SELECT id FROM users WHERE username = :username',
                                {'username': new_username}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id FROM users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast(empty_session):
    empty_session.execute(
        str('INSERT INTO podcasts (title, description, language, website_url) VALUES '
        '("Tech Talks", "A podcast about tech", "English", "https://techtalks.com")')
    )
    row = empty_session.execute('SELECT podcast_id FROM podcasts').fetchone()
    return row[0]


def insert_categories(empty_session):
    empty_session.execute(
        'INSERT INTO categories (category_name) VALUES ("Technology"), ("Business")'
    )
    rows = list(empty_session.execute('SELECT category_id FROM categories'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast_category_associations(empty_session, podcast_key, category_keys):
    stmt = 'INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)'
    for category_key in category_keys:
        empty_session.execute(stmt, {'podcast_id': podcast_key, 'category_id': category_key})


def make_podcast():
    podcast = Podcast(
        1,  # Example ID
        "Tech Talks"
    )
    podcast.description = "A podcast about tech"
    podcast.language = "English"
    podcast.website = "https://techtalks.com"
    return podcast


def make_user():
    user = User(1, "Andrew", "111")
    return user


def make_category():
    category = Category(1, "Technology")
    return category

# Test cases for podcast-related domain objects


def test_loading_of_users(empty_session):
    users = [("Andrew", "1234"), ("Cindy", "1111")]
    insert_users(empty_session, users)

    expected = [User("Andrew", "1234"), User("Cindy", "1111")]
    result = empty_session.query(User).all()

    assert result == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("Andrew", "111")]


def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1, "Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    expected_podcast = make_podcast()
    fetched_podcast = empty_session.query(Podcast).one()

    assert expected_podcast == fetched_podcast
    assert podcast_key == fetched_podcast.id


def test_loading_of_podcast_with_categories(empty_session):
    podcast_key = insert_podcast(empty_session)
    category_keys = insert_categories(empty_session)
    insert_podcast_category_associations(empty_session, podcast_key, category_keys)

    podcast = empty_session.query(Podcast).get(podcast_key)
    categories = [empty_session.query(Category).get(key) for key in category_keys]

    for category in categories:
        assert podcast in category.podcasts


def test_saving_of_podcast(empty_session):
    podcast = make_podcast()
    empty_session.add(podcast)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description, language, website_url FROM podcasts'))
    assert rows == [("Tech Talks", "A podcast about tech", "English", "https://techtalks.com")]


def test_saving_podcast_with_categories(empty_session):
    podcast = make_podcast()
    category = make_category()

    # Establish the bidirectional relationship between the Podcast and the Category.
    podcast.add_category(category)

    # Save the Podcast and Category
    empty_session.add(podcast)
    empty_session.commit()

    # Verify the categories were saved
    rows = list(empty_session.execute('SELECT podcast_id FROM podcasts'))
    podcast_key = rows[0][0]

    rows = list(empty_session.execute('SELECT category_id, category_name FROM categories'))
    category_key = rows[0][0]
    assert rows[0][1] == "Technology"

    # Check that the podcast_categories table has a new record.
    rows = list(empty_session.execute('SELECT podcast_id, category_id FROM podcast_categories'))
    assert podcast_key == rows[0][0]
    assert category_key == rows[0][1]


def test_loading_of_reviewed_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    user_key = insert_user(empty_session)

    # Add a review to the podcast
    empty_session.execute(
        'INSERT INTO reviews (user_id, podcast_id, rating, content) VALUES '
        '(:user_id, :podcast_id, 8, "Great podcast!")',
        {'user_id': user_key, 'podcast_id': podcast_key}
    )

    podcast = empty_session.query(Podcast).one()

    for review in podcast.reviews:
        assert review.podcast is podcast


"""I can't get these to run successfully! Idk what's going wrong."""
