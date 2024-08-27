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
            (category["label"],)  # Ensure "category" is a dictionary and "label" is a valid key
        )

        id = db_cursor.lastrowid

        return json.dumps({"id": id, "label": category["label"]})
