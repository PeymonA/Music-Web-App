from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.exc import NoResultFound

from sqlalchemy.orm import scoped_session

from music.adapters.repository import AbstractRepository
from music.domainmodel.Album import Album
from music.domainmodel.Artist import Artist
from music.domainmodel.Comment import Comment
from music.domainmodel.Genre import Genre
from music.domainmodel.Track import Track
from music.domainmodel.User import User


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def get_all_genres(self):
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def get_users(self):
        users = self._session_cm.session.query(User).all()
        return users

    def get_tracks(self):
        tracks = self._session_cm.session.query(Track).all()
        return tracks

    def number_of_tracks_by_artist(self, artist: Artist):
        pass

    def get_artist_track(self):
        tracks = self._session_cm.session.query(Artist).all()
        return tracks

    def get_album_track(self):
        tracks = self._session_cm.session.query(Album).all()
        return tracks

    def get_number_tracks(self):
        number_of_tracks = self._session_cm.session.query(Track).count()
        return number_of_tracks

    def add_comment(self, comment: Comment):
        super().add_comment(comment)
        with self._session_cm as scm:
            scm.session.add(comment)
            scm.commit()

    def get_comments(self, track_id: int):
        comments = self._session_cm.session.query(Comment).filter(Comment._Comment__track == track_id).one()
        return comments

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.add(artist)
            scm.commit()

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.add(album)
            scm.commit()

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user
