from sqlalchemy import (
    Table, MetaData, Column, Integer, String, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from music.domainmodel.Album import Album
from music.domainmodel.Artist import Artist
from music.domainmodel.Comment import Comment
from music.domainmodel.Genre import Genre
from music.domainmodel.Track import Track
from music.domainmodel.User import User

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)
comments_table = Table(
    'comments', metadata,
    Column('comment_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)
tracks_table = Table(
    'tracks', metadata,
    Column('track_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('album_id', ForeignKey('albums.album_id')),
    Column('artist_id', ForeignKey('artists.id')),
    Column('track_url', String(255), nullable=False),
    Column('track_duration', Integer, nullable=False)
)
genres_table = Table(
    'genres', metadata,
    Column('genre_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)
artists_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False)
)
albums_table = Table(
    'albums', metadata,
    Column('album_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('album_url', String(255), nullable=False),
    Column('album_type', String(255), nullable=False)
)


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__comments': relationship(Comment, backref='_Comment__user')
    })
    mapper(Comment, comments_table, properties={
        '_Comment__comment': comments_table.c.comment,
        '_Comment__track': relationship(Track, backref='_Track__comments'),
        '_Comment__timestamp': comments_table.c.timestamp
    })
    mapper(Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.track_id,
        '_Track__title': tracks_table.c.title,
        '_Track__album': relationship(Album, backref='_Album__track'),
        '_Track__artist': relationship(Artist, backref='_Artist__track'),
        '_Track__track_url': tracks_table.c.track_url,
        '_Track__track_duration': tracks_table.c.track_duration
    })
    mapper(Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.name
    })
    mapper(Artist, artists_table, properties={
        '_Artist__full_name': artists_table.c.full_name
    })
    mapper(Album, albums_table, properties={
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title,
        '_Album__album_url': albums_table.c.album_url,
        '_Album__album_type': albums_table.c.album_type,
    })
