import logging

from flask import Flask

from example_app.views.demo_app import demo_app
from app_error_handler.application_error_handler import register_app_for_error_handling

logging.basicConfig()
LOG = logging.getLogger("DEMO_APP")
LOG.setLevel("DEBUG")
app = Flask(__name__)


def create_app():
    app.register_module(demo_app)
    app.wsgi_app = register_app_for_error_handling(app.wsgi_app, "Demo_App", LOG)
    return app

if __name__ == "__main__":
    app = create_app()
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run()
