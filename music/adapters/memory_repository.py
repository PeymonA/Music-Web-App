import csv


from werkzeug.security import generate_password_hash

from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.repository import AbstractRepository
from music.domainmodel.User import User
from music.domainmodel.Comment import Comment
from music.domainmodel import Artist, Track, Album, Genre


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__genres = list()
        self.__artists = list()
        self.__users = list()
        self.__tracks = list()
        self.__albums = list()
        self.__comments = list()

    def get_all_genres(self):
        return self.__genres

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_users(self) -> list:
        return self.__users

    def get_tracks(self):
        return self.__tracks
        
    def add_comment(self, comment: Comment):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        super().add_comment(comment)
        self.__comments.append(comment)
    
    def number_of_tracks_by_artist(self, artist: Artist):
        count = 0
        for track in self.__tracks:
            if track.artist.artist_id == artist.artist_id:
                count += 1
        return count
    
    def get_artist_track(self):
        return self.__artists

    def get_album_track(self):
        return self.__albums

    def populate(self, albums_file: str, tracks_file: str):
        cvs_reader = TrackCSVReader(albums_file, tracks_file)
        cvs_reader.read_csv_files()
        self.__tracks = cvs_reader.dataset_of_tracks
        self.__artists = cvs_reader.dataset_of_artists
        self.__albums = cvs_reader.dataset_of_albums
        self.__genres = cvs_reader.dataset_of_genres

    def get_number_tracks(self):
        return len(self.__tracks)

    def get_comments(self, track_id):
        return self.__comments[track_id]

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def add_artist(self, artist: Artist):
        self.__artists.append(artist)

    def add_album(self, album: Album):
        self.__albums.append(album)

    def add_track(self, track: Track):
        self.__tracks.append(track)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(users_file: str, repo: MemoryRepository):
    users = dict()

    users_filename = users_file + "/users.csv"
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def populate(users_file: str, repo: MemoryRepository):
    users = load_users(users_file, repo)
