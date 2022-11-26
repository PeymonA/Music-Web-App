import pytest

from music.domainmodel.User import User


def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_number_of_tracks_by_artist(in_memory_repo, artist="PEYMON"):
    tracks = in_memory_repo.number_of_tracks_by_artist(artist)
    assert tracks == 0


def test_get_tracks(in_memory_repo):
    tracks = in_memory_repo.get_tracks()
    assert len(tracks) == in_memory_repo.get_number_tracks()


def test_get_album_track(in_memory_repo):
    tracks = in_memory_repo.get_album_track()
    assert tracks == []


def test_get_artist_track(in_memory_repo):
    tracks = in_memory_repo.get_artist_track()
    assert tracks == []