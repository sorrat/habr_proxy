from urllib.parse import urljoin, urlparse

import requests
from werkzeug.wrappers import Request, Response


SITE_URL = 'https://habr.com'
SITE_DOMAIN = urlparse(SITE_URL).netloc


def execute_request(req: Request) -> dict:
    session = requests.Session()
    # Подготовка запроса вручную нужна для того,
    # чтобы избавиться от ненужных заголовков (headers),
    # которые `requests` добавляет автоматически.
    habr_req = session.prepare_request(requests.Request(
        method=req.method,
        url=urljoin(SITE_URL, req.full_path),
    ))
    # TODO: POST запросы
    habr_req.headers = {
        **req.headers,
        'host': SITE_DOMAIN,
    }
    habr_resp = session.send(habr_req)
    return {
        'response': habr_resp.content,
        'headers': habr_resp.headers.items(),
        'status': habr_resp.status_code,
    }


def handle_request(req: Request) -> Response:
    resp_dict = execute_request(req)
    return Response(**resp_dict)
