import os

from services.server.controllers import auth_user
from services.server.controllers import get_file
from services.server.database.models.user_model import UserModel
from util.pages import pages
from util.request.content_type import content_type
from util.request.response_data import ContentType, HttpStatus
from util.response_data import ResponseData
# CONTROLLER HANDLER
from util.util import read_body, json_to_dict


def app(environ, start_response):
    path = environ.get("PATH_INFO")
    filename, file_extension = os.path.splitext(path)
    if path.endswith("/"):
        path = path[:-1]

    response = ResponseData()
    response.status = "200"

    if path == "":
        response.payload = "The server service is working"

    # Page Requests
    if path.startswith('/static'):
        response = get_file(path)
        response.headers.append(content_type.get(file_extension, ContentType.HTML))
    elif path in pages:
        response = get_file("/templates" + path)
        response.headers = [ContentType.HTML]
    elif path == "/auth_user":
        response = auth_user(environ)
    elif path == '/register_user':
        body = json_to_dict(read_body(environ))
        new_user = UserModel(body['username'], body['firstname'], body['lastname'],
                             body['email'],
                             body['password'])
        response.payload = new_user.save()['message']
    elif path == '/update_user':
        body = json_to_dict(read_body(environ))
        updated_user = UserModel.get_by_id(body['id'])
        if body['username'] != updated_user.username:
            if UserModel.get_by_username(body['username']) is None:
                updated_user.username = body['username']
                updated_user.lastname = body['lastname']
                updated_user.firstname = body['firstname']
                updated_user.email = body['email']
                updated_user.password = body['password']
                if updated_user.is_valid():
                    updated_user.update()
                else:
                    response.status = HttpStatus.BAD_REQUEST
            else:
                response.status = HttpStatus.BAD_REQUEST
    else:
        response.payload = "Not found"
        response.headers = [ContentType.HTML]
        response.status = "404"
    # User Requests

    response.payload = response.payload.encode("utf-8")

    response_headers = [("Content-Length", str(len(response.payload)))]
    response_headers += response.headers

    start_response(

        response.status,
        response_headers
    )
    return iter([response.payload])