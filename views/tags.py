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
            (tag["label"],),  # Ensure "tag" is a dictionary and "label" is a valid key
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
            (data["label"], tagId),
        )

        conn.commit()

    return json.dumps({"message": "Tag updated successfully."})


def delete_tag(tagId):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Tags
            WHERE id = ?
            """,
            (tagId,),
        )

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False

    return True

    
def get_all_tags():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            *
        FROM Tags c
        ORDER BY c.label DESC;
        """
        )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        tags = []
        for row in query_results:
            tags.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_tags = json.dumps(tags)

    return serialized_tags

import sqlite3
import json

def get_tags_for_post(post_id):
    """Fetches tags associated with a specific post from the PostTags join table"""

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the tags associated with the post
        db_cursor.execute(
            """
            SELECT
                t.id, t.label
            FROM Tags t
            JOIN PostTags pt ON t.id = pt.tag_id
            WHERE pt.post_id = ?
            """,
            (post_id,)  # Pass post_id as a parameter to the query
        )

        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        tags = []
        for row in query_results:
            tags.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_tags = json.dumps(tags)

    return serialized_tags

def save_post_tags(post_id, tag_ids):
    """Saves selected tags for a specific post in the PostTags join table"""

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Loop through each tag_id and insert it into the PostTags join table
        for tag_id in tag_ids:
            db_cursor.execute(
                """
                INSERT INTO PostTags (post_id, tag_id)
                VALUES (?, ?)
                """,
                (post_id, tag_id)
            )

        # Commit the changes
        conn.commit()

        # Return a success response
        return json.dumps({"message": "Tags successfully saved for post."})

def get_tag_by_id(tag_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row  # This allows us to fetch rows as dictionaries
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                SELECT 
                    t.id, 
                    t.label
                FROM Tags t
                WHERE t.id = ?
            """,
            (tag_id,),
        )

        row = db_cursor.fetchone()

        if row:
            response = {
                "id": row["id"],
                "label": row["label"]
            }
        else:
            response = None

        return json.dumps(response)