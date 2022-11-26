import abc

from music.domainmodel import User, Artist, Comment, Track, Genre, Album

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_users(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def number_of_tracks_by_artist(self, artist: Artist):
        raise NotImplementedError

    @abc.abstractmethod
    def get_artist_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_album_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_tracks(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_comment(self, comment: Comment):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if comment.user is None or comment not in comment.user.comments:
            raise RepositoryException('Comment not correctly attached to a User')
        if comment.track is None or comment not in comment.track.comments:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_comments(self, track_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, album: Album):
        raise NotImplementedError

    def get_all_genres(self):
        raise NotImplementedError
