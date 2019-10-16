from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse, Request

from app import application


def execute_test_request(req: dict) -> Request:
    c = Client(application, BaseResponse)
    return c.open(**req)
