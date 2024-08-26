import csv

import pytest

from roqueria.main import User, create_user, delete_user, update_user


@pytest.fixture(autouse=True)
def _drop_data_file():
    with open("data/users", "a") as file:
        file.truncate(0)
        yield
        file.truncate(0)


def _get_user(id_: int) -> User:
    with open("data/users", "r") as file:
        csv_reader = csv.reader(file)
        for _ in range(id_):
            next(csv_reader)
        user = next(csv_reader)
        user = User(name=user[0], birthdate=user[1], plan=user[2])
    return user


def test_create_user():
    user_id = create_user("Bill Clinton", "1946/08/19", "CASUAL")
    user = _get_user(user_id)

    assert user == User("Bill Clinton", "1946/08/19", "CASUAL")


def test_create_second_user():
    user_id = create_user("Bill Clinton", "1946/08/19", "CASUAL")
    another_user_id = create_user("Perry Mason", "1984/03/05", "REGULAR")

    assert _get_user(user_id) == User("Bill Clinton", "1946/08/19", "CASUAL")
    assert _get_user(another_user_id) == User("Perry Mason", "1984/03/05", "REGULAR")


def test_update_user():
    user_id = create_user("Bill Clinton", "1946/08/19", "CASUAL")
    update_user(user_id, name="Donald Trump", birthdate="1946/06/14", plan="REGULAR")
    updated_user = _get_user(user_id)
    assert updated_user == User("Donald Trump", "1946/06/14", "REGULAR")


def test_delete_user():
    user_id = create_user("Bill Clinton", "1946/08/19", "CASUAL")
    delete_user(user_id)
    deleted_user = _get_user(user_id)
    assert deleted_user.plan == "DELETED"
