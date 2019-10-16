import random
from urllib.parse import urljoin

from werkzeug.wrappers import BaseResponse

from .helpers import (
    execute_test_request,
)


def test_app(requests_mock):
    req = {
        'method': 'get',
        'path': '/ru/post/123/',
    }
    resp_fixture = build_requests_fixture(req, b'123')
    requests_mock.register_uri(**resp_fixture)

    resp = execute_test_request(req)
    assert resp_fixture['status_code'] == resp.status_code
    assert resp_fixture['headers'] == select_headers(resp, resp_fixture['headers'])
    assert resp_fixture['content'] == resp.data


# -- helpers

def select_headers(resp: BaseResponse, header_names) -> dict:
    return {name: resp.headers.get(name) for name in header_names}


def build_requests_fixture(req, content):
    return {
        'method': req['method'],
        'url': urljoin('https://habr.com', req['path']),
        'content': content,
        'headers': {
            'Content-Type': 'text/html',
            'Set-Cookie': 'UserID=JohnDoe; Max-Age=3600; Version=1',
        },
        'status_code': random.randint(200, 500),
    }
