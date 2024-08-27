import sqlite3
import json

def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.title,
            u.first_name,
            u.last_name, 
            c.label,
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        WHERE p.approved = 1;
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        posts = []
        for row in query_results:
            posts.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_posts = json.dumps(posts)

    return serialized_posts
