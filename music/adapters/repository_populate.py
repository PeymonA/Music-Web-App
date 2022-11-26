import sqlalchemy

from music.adapters.csv_data_importer import load_users
from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.repository import AbstractRepository


def populate_users(users_file: str, repo: AbstractRepository, database_mode: bool):
    # Load users into the repository.
    users = load_users(users_file, repo, database_mode)


def populate(albums_file: str, tracks_file: str, repo: AbstractRepository, database_mode: bool):
    cvs_reader = TrackCSVReader(albums_file, tracks_file)
    cvs_reader.read_csv_files()
    tracks = cvs_reader.dataset_of_tracks
    for i in tracks:
        repo.add_track(i)

    artists = cvs_reader.dataset_of_artists
    check = []
    valid = []
    for names in artists:
        if names.full_name == None or names.full_name == '' or names.full_name == '??ss':
            check.append('Not Valid')
        else:
            check.append(names.full_name)
    check = sorted(check)
    for x in range(len(artists)):
        for y in artists:
            if y.full_name == check[x]:
                valid.append(y)
                break

    for i in valid:
        repo.add_artist(i)

    albums = cvs_reader.dataset_of_albums
    check = []
    valid = []
    for names in albums:
        if names.title == None or names.title == '':
            check.append('Not Valid')
        else:
            check.append(names.title)
    check = sorted(check)
    for x in range(len(albums)):
        for y in albums:
            if y.title == check[x]:
                valid.append(y)
                break

    for i in valid:
        repo.add_album(i)

    genres = cvs_reader.dataset_of_genres
    for i in genres:
        repo.add_genre(i)
