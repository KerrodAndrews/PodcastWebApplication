from flask import Blueprint, render_template, request
from podcast.utilities.services import search_by_podcast_name, search_by_author_name, search_by_category
from podcast.authentication.services import auth_services
from podcast.blueprints.services import *


catalogue_blueprint = Blueprint(
    'search_query_bp', __name__)


@catalogue_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    username = auth_services.get_current_username()
    query = request.args.get('query', '')
    parameter = request.args.get('parameter', 'Title')
    repo_instance = get_repo()
    if parameter == "Author":
        podcasts = search_by_author_name(query, repo_instance) # --------------------------------------
    elif parameter == "Category":
        podcasts = search_by_category(query, repo_instance) # --------------------------------------
    else:
        podcasts = search_by_podcast_name(query, repo_instance) # --------------------------------------
        #Defaults to title if no parameter specified.

    per_page = 10
    total_pages = (len(podcasts) + per_page - 1) // per_page
    page = request.args.get('page', 1, type=int)

    # Takes podcasts depending on page number
    start = (page - 1) * per_page
    end = start + per_page
    items_on_page = podcasts[start:end]

    return render_template('catalogue.html', items_on_page=items_on_page,
                           total_pages=total_pages, page=page, username=username)
