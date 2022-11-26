from music.adapters.repository import AbstractRepository
from music.domainmodel.Comment import make_comment


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def number_of_tracks_by_artist(artist, repo: AbstractRepository):
    return repo.number_of_tracks_by_artist(artist=artist)


def add_comment(track_id: int, comment_text: str, user_name: str, repo: AbstractRepository):
    all_tracks = repo.get_tracks()
    track = None
    for x in all_tracks:
        if int(x.track_id) == int(track_id):
            track = x
    if track is None:
        raise NonExistentTrackException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment_text, user, track)

    # Update the repository.
    repo.add_comment(comment)


def get_tracks(repo: AbstractRepository):
    return repo.get_tracks()


def get_artist_track(repo: AbstractRepository):
    return repo.get_artist_track()


def get_album_track(repo: AbstractRepository):
    return repo.get_album_track()


def get_comments(track_id: int, repo: AbstractRepository):
    return repo.get_comments(track_id)


def get_genres(repo: AbstractRepository):
    return repo.get_all_genres()
