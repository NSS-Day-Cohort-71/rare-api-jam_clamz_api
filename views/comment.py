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


def get_comment_by_id(comment_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row  # This allows us to fetch rows as dictionaries
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                SELECT 
                    c.id, 
                    c.content,
                    p.id as post_id
                FROM Comments c
                JOIN Posts p ON p.id = c.post_id
                WHERE c.id = ?
            """, (comment_id,),
        )

        row = db_cursor.fetchone()

        if row:
            response = {
                "id": row["id"],
                "content": row["content"],
                "post_id": row["post_id"]
            }
        else:
            response = None

        return json.dumps(response)
