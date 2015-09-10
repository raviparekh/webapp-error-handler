import traceback
from flask_error_handler.logging_service import LoggingService
from flask_error_handler.root_exception import RootException
from werkzeug.wrappers import Request


def register_app_for_error_handling(wsgi_app, app_name, app_logger):
    """Wraps a WSGI app and handles uncaught exceptions and defined exception and outputs a the exception in a
    structured format.
    Parameters:
    - wsgi_app is the app.wsgi_app of flask,
    - app_name should in correct format e.g. APP_NAME_1,
    - app_logger is the logger object"""

    logging_service = LoggingService(app_name, app_logger)

    def wrapper(environ, start_response):
        try:
            return wsgi_app(environ, start_response)
        except RootException as e:
            app_request = Request(environ)
            stack_trace = traceback.format_exc().splitlines()[-1]
            logging_service.update_with_exception_data(e, app_request, stack_trace)
        except Exception:
            app_request = Request(environ)
            stack_trace = traceback.format_exc()
            e = RootException("FATAL_000", {}, {}, {}, status_code=500)
            e.error_message = "Unknown System Error"
            logging_service.update_with_exception_data(e, app_request, stack_trace)

        response = logging_service.create_json_error_response()

        return response(environ, start_response)
    return wrapper

