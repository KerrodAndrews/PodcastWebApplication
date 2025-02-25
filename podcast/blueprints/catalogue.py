from flask import Blueprint, render_template, request
from podcast.authentication.services import auth_services
from podcast.blueprints.services import *

catalogue_blueprint = Blueprint(
    'catalogue_bp', __name__)


@catalogue_blueprint.route('/podcasts', methods=['GET'])
def catalogue():
    username = auth_services.get_current_username()
    podcasts = get_podcasts_by_name() # --------------------------------------

    per_page = 10
    total_pages = (len(podcasts) + per_page - 1) // per_page
    page = request.args.get('page', 1, type=int)

    # Takes podcasts depending on page number
    start = (page - 1) * per_page
    end = start + per_page
    items_on_page = podcasts[start:end]

    return render_template('catalogue.html', items_on_page=items_on_page,
                           total_pages=total_pages, page=page, username=username)
