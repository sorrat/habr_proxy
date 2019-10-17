import random
import string
from urllib.parse import urljoin

from werkzeug.wrappers import BaseResponse

from config import settings
from .helpers import (
    execute_test_request,
    binary_data,
    read_fixture,
    html_uniform,
)


def test_binary_request(requests_mock):
    # -- проверка запроса бинарного файла
    req = {
        'method': 'get',
        'path': '/ru/post/123/',
    }
    resp_fixture = build_requests_fixture(req, binary_data())
    requests_mock.register_uri(**resp_fixture)

    resp = execute_test_request(req)
    assert resp_fixture['status_code'] == resp.status_code
    assert resp_fixture['headers'] == select_headers(resp, resp_fixture['headers'])
    assert resp_fixture['content'] == resp.data


def test_html_request(requests_mock):
    # -- проверка запроса html страницы
    req = {
        'method': 'get',
        'path': '/ru/post/123/',
    }
    resp_fixture = build_requests_fixture(req, read_fixture('page_in.html', 'rb'))
    requests_mock.register_uri(**resp_fixture)

    resp = execute_test_request(req)
    assert resp_fixture['status_code'] == resp.status_code
    assert resp_fixture['headers'] == select_headers(resp, resp_fixture['headers'])

    expected_page = (string
        .Template(read_fixture('page_out.html'))
        .substitute({'proxy_address': settings.SITE_URL})
    )
    assert html_uniform(expected_page) == html_uniform(resp.data)


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
