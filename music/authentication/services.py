from werkzeug.security import generate_password_hash, check_password_hash

from music.adapters.repository import AbstractRepository
from music.domainmodel.User import User
from music.domainmodel.Comment import make_comment
from music.tracks.services import *


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

def add_comment(track_id: int, comment_text: str, user_name: str, repo: AbstractRepository):
    all_tracks = repo.get_tracks()
    track = None
    for t in all_tracks:
        if t.track_id == track_id:
            track = 1
            break
    if track is None:
        raise NonExistentTrackException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment_text, user, track)

    # Update the repository.
    repo.add_comment(comment)

def add_user(user_name: str, password: str, repo: AbstractRepository):
    # Check that the given user name is available.
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException
    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)
    # Create and store the new User, with password encrypted.
    user = User(user_name, password_hash)
    repo.add_user(user)


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def get_users(repo: AbstractRepository):
    return repo.get_users()


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'user_name': user.user_name,
        'password': user.password
    }
    return user_dict
