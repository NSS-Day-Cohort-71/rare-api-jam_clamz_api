import sqlite3
import json

def create_comment(data):
    """
    Args:
        data (dict): A dictionary containing the post details

    Returns:
        json string: A success message if the post is created successfully
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Write the SQL query to insert a new comment
        db_cursor.execute(
            """
        INSERT INTO Comments (post_id, author_id, content, date)
        VALUES (?, ?, ?, ?)
        """,
            (
                data["post_id"],
                data["author_id"],
                data["content"],
                data["date"]
            ),
        )

        # Commit the transaction
        conn.commit()

    return json.dumps({"message": "Comment created successfully"})