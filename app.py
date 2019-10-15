from werkzeug.wrappers import Request, Response

import settings


@Request.application
def application(request):
    return Response('Hello, World!')


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(settings.HOST, settings.PORT, application,
               use_debugger=True, use_reloader=True)
