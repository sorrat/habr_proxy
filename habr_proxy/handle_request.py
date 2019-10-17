from urllib.parse import urljoin, urlparse

import requests
from werkzeug.wrappers import Request, Response


TARGET_SITE_URL = 'https://habr.com'
TARGET_SITE_DOMAIN = urlparse(TARGET_SITE_URL).netloc


def exclude_keys(dct, keys):
    return {k: v for k, v in dct.items() if k not in keys}


def execute_request(req: Request) -> dict:
    # TODO: проверить POST запросы
    habr_req = {
        'method': req.method,
        'url': urljoin(TARGET_SITE_URL, req.full_path),
        'data': req.data,
        'files': req.files,
        'cookies': req.cookies,
        'headers': {
            **req.headers,
            'host': TARGET_SITE_DOMAIN,
        },
    }
    habr_resp = requests.request(**habr_req)
    return {
        'response': habr_resp.content,
        # Удаление заголовка 'Content-Encoding' с неправильным значением
        'headers': exclude_keys(habr_resp.headers, ['Content-Encoding']),
        'status': habr_resp.status_code,
    }


def handle_request(req: Request) -> Response:
    resp_dict = execute_request(req)
    return Response(**resp_dict)
