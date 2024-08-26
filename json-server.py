import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

# non-boilerplate import
from views import create_user, login_user


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for kneel diamonds"""

    def do_GET(self):
        """Handle GET requests"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "Users":
            if url["pk"]:
                response_body = login_user(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            else:
                return self.response(
                    "User does not exist in the database. Please register your account.",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

    def do_POST(self):
        """Handle POST requests"""

        url = self.parse_url(self.path)

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "register":
            successfully_created = create_user(request_body)
            if successfully_created:
                return self.response(
                    "Your account has been created.",
                    status.HTTP_201_SUCCESS_CREATED.value,
                )
            else:
                return self.response(
                    "Your account could not be created.",
                    status.HTTP_500_SERVER_ERROR.value,
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
