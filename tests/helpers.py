import os

from bs4 import BeautifulSoup
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse, Request

from config import root
from app import application


def execute_test_request(req: dict) -> Request:
    c = Client(application, BaseResponse)
    return c.open(**req)


def binary_data() -> bytes:
    return os.urandom(32)


def read_fixture(name, mode='r'):
    path = root('tests/fixtures', name)
    with open(path, mode) as f:
        return f.read()


def html_uniform(html_text) -> str:
    return BeautifulSoup(html_text, 'html5lib').prettify()
