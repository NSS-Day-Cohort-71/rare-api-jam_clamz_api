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
