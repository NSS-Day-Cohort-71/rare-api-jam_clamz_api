import sqlite3
import json


def create_tag(tag):
    """Creates a new tag in the database"""

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Tags (label)
            VALUES (?)
            """,
            (
                tag["label"],
            ),  # Ensure "tag" is a dictionary and "label" is a valid key
        )

        id = db_cursor.lastrowid

        return json.dumps({"id": id, "label": tag["label"]})
    
def edit_tag(tagId, data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                UPDATE Tags
                SET
                    label = ?
                WHERE id = ?
            """, 
            (data["label"], tagId)
        )

        conn.commit()

    return json.dumps({"message": "Tag updated successfully."}) 