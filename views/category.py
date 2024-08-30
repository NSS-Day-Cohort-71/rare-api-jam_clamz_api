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


def delete_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Categories WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def edit_category(pk, new_label):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Execute the SQL query to update the category's label
        db_cursor.execute(
            """
            UPDATE Categories
            SET label = ?
            WHERE id = ?
            """,
            (new_label["label"], pk),
        )

        # Check if the category was updated
        if db_cursor.rowcount == 0:
            return None  # Return None if no rows were updated

        # Fetch the updated category from the database
        db_cursor.execute(
            """
            SELECT * FROM Categories WHERE id = ?
            """,
            (pk,),
        )
        updated_category = db_cursor.fetchone()

    # Convert the updated category row to a dictionary and return it
    return dict(updated_category) if updated_category else None
