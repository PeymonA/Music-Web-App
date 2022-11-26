import csv

from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository
from music.domainmodel.User import User


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


def load_users(users_file: str, repo: AbstractRepository, database_mode: bool):
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
