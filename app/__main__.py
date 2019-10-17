from werkzeug.serving import run_simple

from config import settings
from .app import application


run_simple(
    settings.HOST,
    settings.PORT,
    application,
    use_debugger=True,
    use_reloader=True
)
