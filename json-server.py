import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

# non-boilerplate import

from views import (
    create_user,
    login_user,
    get_all_posts,
    get_user,
    create_post,
    get_posts_by_user_id,
    create_category,
    get_all_categories,
    delete_category,
    get_post_by_id,
    edit_category,
    edit_post,
    delete_post,
    get_comments_by_post_id,
    create_comment,
    create_tag,
    delete_comment,
    get_comment_by_id,
    edit_comment,
    edit_tag,
    delete_tag,
    get_all_tags,
    get_tags_for_post,
    save_post_tags,
)


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for kneel diamonds"""

    def do_GET(self):
        """Handle GET requests"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "Users":
            if url["pk"]:
                response_body = get_user(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            else:
                return self.response(
                    "User does not exist in the database. Please register your account.",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )
        elif url["requested_resource"] == "Posts":
            if url["pk"]:
                response_body = get_post_by_id(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                response_body = get_all_posts()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
        elif url["requested_resource"] == "My-Posts":
            user_id = url["query_params"].get("userId")
            if user_id:
                # Extract the user ID from the list
                if isinstance(user_id, list):
                    user_id = user_id[0] if user_id else None

                # Try to convert to integer
                try:
                    user_id = int(user_id)
                except ValueError:
                    return self.response(
                        json.dumps({"error": "Invalid user ID"}),
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )

                response_body = get_posts_by_user_id(user_id)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                return self.response(
                    json.dumps({"error": "UserId is required for My-Posts request."}),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

        elif url["requested_resource"] == "category":
            response_body = get_all_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        elif url["requested_resource"] == "tags":
            response_body = get_all_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "posttags":
            post_id = url["query_params"].get("post_id", None)
        if post_id:
            response = get_tags_for_post(post_id[0])  # Fetch the tags for the specific post
            return self.response(response, status.HTTP_200_SUCCESS.value)


        elif url["requested_resource"] == "Comments":
            post_id = url["query_params"].get("post_id")
            pk = url["pk"]

            if post_id:
                # this ensures post_id is a single value
                if isinstance(post_id, list):
                    post_id = post_id[0] if post_id else None

                response_body = get_comments_by_post_id(post_id)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            elif pk:
                response_body = get_comment_by_id(pk)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                return self.response(
                    json.dumps({"error": "post_id is required for Comments request."}),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

    def do_POST(self):
        """Handle POST requests"""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "register":
            # Get the request body JSON for the new data
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)

            response_body = create_user(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "login":
            # Get the request body JSON for the new data
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)

            response_body = login_user(request_body)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "category":
            # Get the request body JSON for the new data
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)

            response_body = create_category(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "Posts":
            # Get the request body JSON for the new post
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)

            response_body = create_post(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "tags":
            # Get the request body JSON for the new data
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)

            response_body = create_tag(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)
        
        elif url["requested_resource"] == "posttags":
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            data = json.loads(request_body)

            post_id = data.get("post_id")
            tag_ids = data.get("tag_ids")

            if post_id and tag_ids:
                response = save_post_tags(post_id, tag_ids)  # Save tags for the specific post
                return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "Comments":
            # Get the request body JSON for the new post
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)

            response_body = create_comment(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        else:
            return self.response(
                "Resource not found. Please check your request URL.",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def do_DELETE(self):
        """Handle DELETE requests"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "category":
            if pk != 0:
                successfully_deleted = delete_category(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        elif url["requested_resource"] == "Posts":
            if pk != 0:
                successfully_deleted = delete_post(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )
        elif url["requested_resource"] == "Comments":
            if pk != 0:
                successfully_deleted = delete_comment(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        elif url["requested_resource"] == "Tags":
            if pk != 0:
                successfully_deleted = delete_tag(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

    def do_PUT(self):
        """Handle PUT requests"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "category":
            if pk != 0:
                response_body = edit_category(pk, request_body)

                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "Posts":
            if pk != 0:
                response_body = edit_post(pk, request_body)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "Comments":
            if pk != 0:
                response_body = edit_comment(pk, request_body)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "Tags":
            if pk != 0:
                response_body = edit_tag(pk, request_body)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            self.response(
                "Resource not found. Please check your request URL.",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
