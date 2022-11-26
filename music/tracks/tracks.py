from better_profanity import profanity
from flask import Blueprint, render_template, url_for, request, session
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import ValidationError, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

import music.adapters.repository as repo
import music.utilities.utilities as utilities
from music.authentication.authentication import login_required
from music.tracks import services

tracks_blueprint = Blueprint('tracks_bp', __name__)


@tracks_blueprint.route('/browse_artists', methods=['GET'])
def browse_artists():
    page = request.args.get('page', 0, type=int)
    length = 10
    track_min = page * length
    tracks = []
    check = []
    all_tracks = services.get_artist_track(repo.repo_instance)
    size = len(all_tracks) // length

    first_track_url = url_for('tracks_bp.browse_artists', page=0)
    next_track_url = url_for('tracks_bp.browse_artists', page=page + 1)
    prev_track_url = url_for('tracks_bp.browse_artists', page=page - 1)
    last_track_url = url_for('tracks_bp.browse_artists', page=size)

    if page == 0:
        prev_track_url = None
        first_track_url = None

    if (page + 1) * length >= len(all_tracks):
        last_track_url = None
        next_track_url = None

    if page * length >= len(all_tracks) or page < 0:
        return redirect(url_for('tracks_bp.browse_artists', page=0))

    number = 0
    count = track_min
    while number != length:
        if len(tracks) < length and count < len(all_tracks):
            if all_tracks[count].full_name not in check:
                tracks.append((all_tracks[count],
                               services.number_of_tracks_by_artist(all_tracks[count], repo.repo_instance)))
                check.append(all_tracks[count].full_name)
                number += 1
        else:
            number = length
        count += 1

    return render_template(
        'music/browse_artists.html',
        title='Artists',
        artist_title='Search by Artists',
        tracks=tracks,
        next_track_url=next_track_url,
        first_track_url=first_track_url,
        prev_track_url=prev_track_url,
        last_track_url=last_track_url
    )


@tracks_blueprint.route('/browse_album', methods=['GET'])
def browse_album():
    page = request.args.get('page', 0, type=int)
    length = 10
    track_min = page * length
    track_max = track_min + length
    tracks = []
    all_tracks = services.get_album_track(repo.repo_instance)
    my_tracks = services.get_tracks(repo.repo_instance)
    size = len(all_tracks) // length

    first_track_url = url_for('tracks_bp.browse_album', page=0)
    next_track_url = url_for('tracks_bp.browse_album', page=page + 1)
    prev_track_url = url_for('tracks_bp.browse_album', page=page - 1)
    last_track_url = url_for('tracks_bp.browse_album', page=size)

    if page == 0:
        prev_track_url = None
        first_track_url = None

    if (page + 1) * length >= len(all_tracks):
        last_track_url = None
        next_track_url = None

    if page * length >= len(all_tracks) or page < 0:
        return redirect(url_for('tracks_bp.browse_album', page=0))

    for count in range(track_min, track_max):
        if len(tracks) < length and count < len(all_tracks):
            for names in my_tracks:
                if names.album != None and (all_tracks[count], names.album.title) not in tracks:
                    if names.album.title == all_tracks[count].title:
                        tracks.append((all_tracks[count], names.artist.full_name))
                        break

    return render_template(
        'music/browse_album.html',
        title='Albums',
        album_title='Search by Albums',
        tracks=tracks,
        next_track_url=next_track_url,
        first_track_url=first_track_url,
        prev_track_url=prev_track_url,
        last_track_url=last_track_url
    )


@tracks_blueprint.route('/browse_tracks', methods=['GET'])
def browse_tracks():
    page = request.args.get('page', 0, type=int)
    length = 10
    track_min = page * length
    track_max = track_min + length
    tracks = []
    all_tracks = services.get_tracks(repo.repo_instance)
    size = len(all_tracks) // length

    first_track_url = url_for('tracks_bp.browse_tracks', page=0)
    next_track_url = url_for('tracks_bp.browse_tracks', page=page + 1)
    prev_track_url = url_for('tracks_bp.browse_tracks', page=page - 1)
    last_track_url = url_for('tracks_bp.browse_tracks', page=size - 1)

    if page == 0:
        prev_track_url = None
        first_track_url = None

    if (page + 1) * length >= len(all_tracks):
        last_track_url = None
        next_track_url = None

    if page * length >= len(all_tracks) or page < 0:
        return redirect(url_for('tracks_bp.browse_tracks', page=0))

    for count in range(track_min, track_max):
        if len(tracks) < length and count < len(all_tracks):
            tracks.append(all_tracks[count])

    return render_template(
        'music/browse_tracks.html',
        title='Tracks',
        tracks_title='Search by Tracks',
        tracks=tracks,
        next_track_url=next_track_url,
        first_track_url=first_track_url,
        prev_track_url=prev_track_url,
        last_track_url=last_track_url
    )


@tracks_blueprint.route('/browse_genre', methods=['GET'])
def browse_genre():
    page = request.args.get('page', 0, type=int)
    length = 10
    track_min = page * length
    track_max = track_min + length
    tracks = []
    all_tracks = services.get_genres(repo.repo_instance)
    size = len(all_tracks) // length

    first_track_url = url_for('tracks_bp.browse_genre', page=0)
    next_track_url = url_for('tracks_bp.browse_genre', page=page + 1)
    prev_track_url = url_for('tracks_bp.browse_genre', page=page - 1)
    last_track_url = url_for('tracks_bp.browse_genre', page=size - 1)

    if page == 0:
        prev_track_url = None
        first_track_url = None

    if (page + 1) * length >= len(all_tracks):
        last_track_url = None
        next_track_url = None

    if page * length >= len(all_tracks) or page < 0:
        return redirect(url_for('tracks_bp.browse_genre', page=0))

    for count in range(track_min, track_max):
        if len(tracks) < length and count < len(all_tracks):
            tracks.append(all_tracks[count])

    return render_template(
        'music/browse_genre.html',
        title='Tracks',
        genre_name='Search by Genres',
        tracks=tracks,
        next_track_url=next_track_url,
        first_track_url=first_track_url,
        prev_track_url=prev_track_url,
        last_track_url=last_track_url
    )


@tracks_blueprint.route('/view_track_comments', methods=['GET'])
def view_track_comments():
    valid = None
    tracks_to_show_comments = request.args.get('view_comments_for')
    for x in services.get_tracks(repo.repo_instance):
        if int(x.track_id) == int(tracks_to_show_comments):
            valid = x

    return render_template(
        'music/view_comment.html',
        title=valid.title,
        track=valid,
    )


@tracks_blueprint.route('/simple_track_view/<id>', methods=['GET', 'POST'])
def simple_track_view(id):
    for x in services.get_tracks(repo.repo_instance):
        if int(x.track_id) == int(id):
            return redirect(url_for('tracks_bp.view_track_comments', view_comments_for=id))


@tracks_blueprint.route('/simple_track/<id>', methods=['GET', 'POST'])
@login_required
def simple_track(id):
    user_name = session['user_name']
    form = ReviewForm()
    handler_url = None
    all_tracks = services.get_tracks(repo.repo_instance)
    valid = None
    if form.validate_on_submit():
        for x in all_tracks:
            if int(x.track_id) == int(id):
                valid = x

        track_id = id
        services.add_comment(track_id, form.comment.data, user_name, repo.repo_instance)

        return redirect(url_for('tracks_bp.view_track_comments', view_comments_for=id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        track_id = request.args.get('id')

        # Store the article id in the form.
        form.track_id.data = track_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        track_id = int(form.track_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    for x in all_tracks:
        if int(x.track_id) == track_id:
            valid = x
    return render_template(
        'music/simple_track.html',
        title='Track title',
        track=valid,
        form=form,
        comment=None,
        handler_url=url_for('tracks_bp.simple_track', id=id)
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    comment = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your Review is too short'),
        ProfanityFree(message='Your Review must not contain profanity')])
    track_id = HiddenField("Track id")
    submit = SubmitField('Submit')
