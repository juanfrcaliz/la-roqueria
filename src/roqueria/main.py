import csv
from dataclasses import dataclass
from enum import Enum


class Plan(str, Enum):
    CASUAL = "CASUAL"
    REGULAR = "REGULAR"
    PRO = "PRO"
    DELETED = "DELETED"


@dataclass(frozen=True)
class User:
    name: str
    birthdate: str  # should be a datetime.date
    plan: Plan


# Does it make sense to create this as a helper function?
# Should it be a private function?
def _parse_csv_user(unparsed_user: list) -> User:
    user = User(name=unparsed_user[0], birthdate=unparsed_user[1], plan=unparsed_user[2])

    return user


def create_user(name: str, birthdate: str, plan: Plan) -> int:
    path = "data/users"
    new_user = User(name, birthdate, plan)

    with open(path, "r+") as file:
        csv_reader = csv.reader(file)
        user_id = sum(1 for _ in csv_reader)

        csv_writer = csv.writer(file)
        csv_writer.writerow(
            [new_user.name, new_user.birthdate, new_user.plan]  # not a big improvement, but checks the type
        )

    return user_id


def get_user(id: int) -> User:
    user_file = "data/users"
    with open(user_file, "r") as file:
        csv_reader = csv.reader(file)
        for _ in range(id):
            next(csv_reader)
        user = _parse_csv_user(next(csv_reader))

    return user


def update_user(user_id: int, name: str = None, birthdate: str = None, plan: Plan = None):
    users = []
    with open("data/users", "r") as csvfile:
        reader = csv.reader(csvfile)
        id_ = 0
        for row in reader:
            if id_ == user_id:
                # Update the user's information if the id matches
                if name is not None:
                    row[0] = name
                if birthdate is not None:
                    row[1] = birthdate
                if plan is not None:
                    row[2] = plan
            users.append(row)
            id_ += id_

    # Write the updated users back to the file
    with open("data/users", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(users)


def delete_user(user_id: int):
    update_user(user_id=user_id, plan="DELETED")
