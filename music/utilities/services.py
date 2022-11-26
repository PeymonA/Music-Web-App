from random import random
from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel import Genre
from music.domainmodel.Track import Track


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


