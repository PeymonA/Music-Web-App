from __future__ import annotations
from datetime import datetime

from typing import List

from music.domainmodel import User
from music.domainmodel.Track import Track


class Comment:
    def __init__(self, user: User, track: 'Track', comment: str, timestamp: datetime):
        self.__user: User = user
        self.__track: Track = track
        self.__comment: str = comment
        self.__timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self.__user

    @property
    def track(self) -> 'Track':
        return self.__track

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other.user == self.user and other.track == self.track and \
               other.comment == self.comment and other.timestamp == self.timestamp


def make_comment(comment_text: str, user: User, track: Track, timestamp: datetime = datetime.today()):
    comment = Comment(user, track, comment_text, timestamp)
    user.add_comment(comment)
    track.add_comment(comment)
    return comment
