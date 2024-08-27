import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {"valid": True, "token": user_from_db["id"]}
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})


def get_user(pk):
    """Retrieves a user from the database by primary key (id)

    Args:
        pk (int): The primary key of the user to retrieve

    Returns:
        json string: Contains the user data if found, otherwise indicates the user was not found
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT id, first_name, last_name, username, email, bio, created_on, active
            FROM Users
            WHERE id = ?
            """,
            (pk,),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            user = {
                "id": user_from_db["id"],
                "first_name": user_from_db["first_name"],
                "last_name": user_from_db["last_name"],
                "username": user_from_db["username"],
                "email": user_from_db["email"],
                "bio": user_from_db["bio"],
                "created_on": user_from_db["created_on"],
                "active": user_from_db["active"],
            }
            response = {"found": True, "user": user}
        else:
            response = {"found": False}

        return json.dumps(response)
