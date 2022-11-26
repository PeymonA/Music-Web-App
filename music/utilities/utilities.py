from flask import Blueprint, request, render_template, redirect, url_for, session

import music.adapters.repository as repo
import music.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


# Takes in get_tracks_a() from music.utilities.services.py with the example 'Food'
def get_tracks_aa():
    track_names = services.get_tracks_a(repo.repo_instance)
    a = [x for x in track_names if track_names != False]

    return a


def get_selected_tracks(quantity=3):
    tracks = services.get_random_tracks(quantity, repo.repo_instance)

    for track in tracks:
        track['hyperlink'] = url_for('home_bp.browse_by_title', track=track['title'])
    return tracks
