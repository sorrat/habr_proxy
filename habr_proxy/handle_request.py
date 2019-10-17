import re
from urllib.parse import urljoin, urlparse

import requests
from werkzeug.wrappers import Request, Response

from config import settings
from .inject_tm import inject_tm_html


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


def localize_page_links(text: str) -> str:
    return re.sub(
        r'href="%s' % TARGET_SITE_URL,
        r'href="%s' % (settings.SITE_URL),
        text,
    )


def edit_html(content: bytes) -> bytes:
    if b'doctype' not in content[:10].lower():
        return content
    text = content.decode()
    text = localize_page_links(text)
    text = inject_tm_html(text)
    return text.encode()


def edit_response(resp: dict) -> dict:
    return {
        **resp,
        'response': edit_html(resp['response']),
    }


def handle_request(req: Request) -> Response:
    resp = execute_request(req)
    resp = edit_response(resp)
    return Response(**resp)
