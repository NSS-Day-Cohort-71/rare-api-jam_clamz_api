import sqlite3
import json


def create_category(category):
    """Creates a new category in the database"""

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Categories (label)
            VALUES (?)
            """,
            (
                category["label"],
            ),  # Ensure "category" is a dictionary and "label" is a valid key
        )

        id = db_cursor.lastrowid

        return json.dumps({"id": id, "label": category["label"]})


def get_all_categories():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            *
        FROM Categories c
        ORDER BY c.label DESC;
        """
        )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        categories = []
        for row in query_results:
            categories.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_categories = json.dumps(categories)

    return serialized_categories
