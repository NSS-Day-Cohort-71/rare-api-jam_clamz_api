import sqlite3
import json


def get_comments_by_post_id(post_id):
    """Get all comments for a post, including author details"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                c.id,
                c.post_id,
                c.author_id,
                c.content,
                c.date,
                u.username
            FROM Comments c
            JOIN Users u ON u.id = c.author_id
            WHERE c.post_id = ?
            ORDER BY c.date DESC
            """,
            (post_id,),
        )

        comments = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = {
                "id": row["id"],
                "post_id": row["post_id"],
                "author_id": row["author_id"],
                "content": row["content"],
                "date": row["date"],
                "author": {"username": row["username"]},
            }
            comments.append(comment)

    return json.dumps(comments)


def delete_comment(comment_id):
    """Delete a comment by id"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Comments
            WHERE id = ?
            """,
            (comment_id,),
        )

        conn.commit()

        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


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
            (data["post_id"], data["author_id"], data["content"], data["date"]),
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
            """,
            (comment_id,),
        )

        row = db_cursor.fetchone()

        if row:
            response = {
                "id": row["id"],
                "content": row["content"],
                "post_id": row["post_id"],
            }
        else:
            response = None

        return json.dumps(response)


def edit_comment(comment_id, data):

    content = data["content"]

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                UPDATE Comments 
                SET 
                    content = ?
                WHERE id = ?
            """,
            (
                content,
                comment_id,
            ),
        )

        conn.commit()

    return json.dumps({"message": "Comment updated successfully."})
