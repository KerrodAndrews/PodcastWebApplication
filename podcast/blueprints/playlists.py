from flask import Blueprint, render_template, request, session, redirect, url_for
from podcast.blueprints.services import *
from podcast.domainmodel.model import Playlist

playlists_blueprint = Blueprint(
    'playlists_bp', __name__)


@playlists_blueprint.route('/playlists', methods=['GET', 'POST'])
def playlists():
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))

    user = get_user(session['username']) # --------------------------------------
    user_playlists = get_playlists_by_user(user) # --------------------------------------

    return render_template('playlists.html', playlists=user_playlists, username=session['username'])


@playlists_blueprint.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))

    user = get_user(session['username']) # --------------------------------------
    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        if playlist_name:
            playlist_id = get_next_playlist_id() # --------------------------------------
            new_playlist = Playlist(playlist_id=playlist_id, playlist_name=playlist_name, user=user)
            add_playlist(new_playlist) # --------------------------------------
            return redirect(url_for('playlists_bp.playlists'))


@playlists_blueprint.route('/playlists/add_podcast/<int:podcast_id>', methods=['GET','POST'])
def add_podcast_to_playlist(podcast_id):
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))

    playlist_id = request.form.get('playlist_id')
    playlist = get_playlist(int(playlist_id)) # --------------------------------------
    podcast = get_podcast(podcast_id) # --------------------------------------

    if playlist and podcast:
        playlist.add_podcast(podcast)
        save_playlist(playlist) # --------------------------------------
    return redirect(url_for('podcast_description_bp.podcast_description', podcast_id=podcast_id))


@playlists_blueprint.route('/playlists/add_episode/<string:episode_title>', methods=['GET','POST'])
def add_episode_to_playlist(episode_title):
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))

    playlist_id = request.form.get('playlist_id')
    podcast_id = request.form.get('podcast_id')
    playlist = get_playlist(int(playlist_id)) # --------------------------------------
    episode = get_episode_by_title(episode_title) # --------------------------------------
    playlist.playlist_add(episode) # --------------------------------------
    save_playlist(playlist) # --------------------------------------

    return redirect(url_for('podcast_description_bp.podcast_description', podcast_id=podcast_id))


@playlists_blueprint.route('/playlists/remove_podcast/<int:playlist_id>/<string:podcast_title>', methods=['POST'])
def remove_podcast_from_playlist(playlist_id, podcast_title):
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))

    user = get_user(str(session['username'])) # --------------------------------------
    playlist = get_playlist(playlist_id) # --------------------------------------

    if playlist and playlist.user == user:
        podcast = get_podcast_by_title(podcast_title) # --------------------------------------
        if podcast:
            playlist.remove_podcast(podcast)
            save_playlist(playlist) # --------------------------------------

    return redirect(url_for('playlists_bp.playlists'))

@playlists_blueprint.route('/playlists/remove_episode/<int:playlist_id>/<string:episode_title>', methods=['POST'])
def remove_episode_from_playlist(playlist_id, episode_title):
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))

    user = get_user(session['username']) # --------------------------------------
    playlist = get_playlist(playlist_id) # --------------------------------------
    if playlist and playlist.user == user:
        episode = get_episode_by_title(episode_title) # --------------------------------------
        if episode:
            playlist.remove_episode(episode)
            save_playlist(playlist) # --------------------------------------

    return redirect(url_for('playlists_bp.playlists'))
