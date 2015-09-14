from flask import Response, Module

from example_app.services.authication_service import validate_user

demo_app = Module(__name__)


@demo_app.route("/login/<user_name>/<passwd>", methods=['POST'])
def login(user_name, passwd):
    validate_user(user_name, passwd)
    return Response('Logged in', status=200)

