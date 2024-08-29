import sqlite3
import json


def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            p.id,
            p.title,
            p.user_id,
            u.first_name,
            u.last_name, 
            c.label
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        WHERE p.approved = 1
        ORDER BY p.publication_date DESC;
        """
        )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        posts = []
        for row in query_results:
            posts.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_posts = json.dumps(posts)

    return serialized_posts


def get_post_by_id(post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                p.title,
                p.image_url,
                p.category_id,
                p.content,
                p.user_id, 
                strftime('%m/%d/%Y', p.publication_date) as publication_date,
                u.first_name,
                u.last_name
            FROM Posts p
            JOIN Users u ON u.id = p.user_id
            WHERE p.id = ?
            """,
            (post_id,),
        )

        query_results = db_cursor.fetchone()

        result = dict(query_results) if query_results else None

    return json.dumps(result)


def create_post(data):
    """
    Args:
        data (dict): A dictionary containing the post details

    Returns:
        json string: A success message if the post is created successfully
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Check if 'author' key exists in the dictionary
        if "author" not in data:
            print("Error: 'author' key is missing from the data dictionary")
            return json.dumps({"error": "'author' key is missing"})

        # Write the SQL query to insert a new post
        db_cursor.execute(
            """
        INSERT INTO Posts (title, content, category_id, publication_date, image_url, user_id, approved)
        VALUES (?, ?, ?, ?, ?, (SELECT id FROM Users WHERE first_name = ?), ?)
        """,
            (
                data["title"],
                data["content"],
                data[
                    "category"
                ],  # Here we directly use the categoryId passed from the front end
                data["publicationDate"],
                data["headerImageUrl"],
                data["author"],
                data["approved"],
            ),
        )

        # Commit the transaction
        conn.commit()

    return json.dumps({"message": "Post created successfully"})


def get_posts_by_user_id(user_id):
    """
    Args:
        user_id (int): The user ID to filter posts by

    Returns:
        json string: A JSON string containing the list of posts with user details
    """
    # Extract the user_id from the list if it's in that format
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the posts by user ID with expanded user details
        db_cursor.execute(
            """
            SELECT
                p.id,
                p.title,
                p.content,
                u.first_name,
                u.last_name, 
                c.label
            FROM Posts p
            JOIN Users u ON u.id = p.user_id
            JOIN Categories c ON c.id = p.category_id
            WHERE p.user_id = ?;
            """,
            (user_id,),
        )
        query_results = db_cursor.fetchall()

        # Serialize Python dictionary to JSON encoded string
        serialized_posts = json.dumps([dict(row) for row in query_results])

    return serialized_posts


import sqlite3
import json


def edit_post(post_id, data):
    """
    Args:
        post_id (int): The ID of the post to be edited
        data (dict): A dictionary containing the updated post details

    Returns:
        json string: A success message if the post is updated successfully
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Check if required keys exist in the dictionary
        required_keys = [
            "title",
            "content",
            "category",
            "publicationDate",
            "headerImageUrl",
            "author",
            "approved",
        ]
        for key in required_keys:
            if key not in data:
                print(f"Error: '{key}' key is missing from the data dictionary")
                return json.dumps({"error": f"'{key}' key is missing"})

        query = """
            UPDATE Posts
            SET 
                title = ?,
                content = ?,
                category_id = ?,
                publication_date = ?,
                image_url = ?,
                user_id = (SELECT id FROM Users WHERE first_name = ?),
                approved = ?
            WHERE id = ?
        """

        db_cursor.execute(
            query,
            (
                data["title"],
                data["content"],
                data["category"],
                data["publicationDate"],
                data["headerImageUrl"],
                data["author"],
                data["approved"],
                post_id,
            ),
        )

        # Commit the transaction
        conn.commit()

        # Verify the update
        db_cursor.execute("SELECT * FROM Posts WHERE id = ?", (post_id,))
        updated_post = db_cursor.fetchone()

    return json.dumps({"message": "Post updated successfully."})
