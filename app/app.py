from werkzeug.wrappers import Request, Response

import habr_proxy


@Request.application
def application(request) -> Response:
    return habr_proxy.handle_request(request)
