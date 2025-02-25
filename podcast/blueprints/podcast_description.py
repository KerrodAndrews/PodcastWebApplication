from flask import Blueprint, render_template, request, session, redirect, url_for
from podcast.domainmodel.model import Review
from podcast.authentication.services import auth_services
from podcast.blueprints.services import *

podcast_description_blueprint = Blueprint(
    'podcast_description_bp', __name__)


@podcast_description_blueprint.route('/description/<int:podcast_id>', methods=['GET', 'POST'])
def podcast_description(podcast_id):
    username = auth_services.get_current_username()
    podcast = get_podcast(podcast_id) # --------------------------------------
    print(podcast)
    episodes = get_episodes_for_podcast(podcast_id) # --------------------------------------

    per_page = 5
    total_pages = (len(episodes) + per_page - 1) // per_page
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * per_page
    end = start + per_page
    items_on_page = episodes[start:end]

    # Review

    if request.method == "POST":
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login')) # redirect to login page
        user = get_user(session['username']) # --------------------------------------
        rating = request.form.get('rating', type=int)
        content = request.form.get('content')

        # Make a review and save it for the session
        review = Review(review_id=get_length()+1, user=user, rating=rating, content=content, podcast_id=podcast_id)
        #podcast.reviews.append(review)

        save_review(review)
        return redirect(url_for('podcast_description_bp.podcast_description', podcast_id=podcast_id))

    average_rating = sum([review._rating for review in get_review(podcast_id)]) / len(get_review(podcast_id)) if get_review(podcast_id) else 0
    sorted_reviews = sorted(get_review(podcast_id), key=lambda x: x._rating, reverse=True)
    user_playlists = []
    if 'username' in session:
        user = get_user(session['username']) # --------------------------------------
        user_playlists = get_playlists_by_user(user) # --------------------------------------

    return render_template('podcastDescription.html', podcast=podcast,
                           episodes=episodes,
                           items_on_page=items_on_page,
                           total_pages=total_pages, page=page,
                           average_rating=average_rating,podcast_id=podcast_id, reviews=sorted_reviews,
                           user_playlists=user_playlists, username=username)
