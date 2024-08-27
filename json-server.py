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
), create_category


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
                response_body = get_posts_by_user_id(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                response_body = get_all_posts()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

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
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "Posts":
            # Get the request body JSON for the new post
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)

            response_body = create_post(request_body)
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

        pass

    def do_PUT(self):
        """Handle PUT requests"""

        url = self.parse_url(self.path)

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        pass


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
    