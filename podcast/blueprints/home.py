from flask import Blueprint, render_template, session
from podcast.authentication.services import auth_services
from podcast.blueprints.services import *
from podcast.adapters.repo_utils import get_random_podcasts

home_blueprint = Blueprint(
        'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    # Returns an empty string if there is no session cookie
    username = auth_services.get_current_username()

    return render_template(
        'layout.html', podcasts=get_random_podcasts(15, get_repo()),
        username=username
    )
