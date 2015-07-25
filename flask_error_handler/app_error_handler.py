import json
import traceback
import uuid
from flask_error_handler.root_exception import RootException
from flask import Response, request


def register_app_for_error_handling(wsgi_app, app_name, app_logger):
    """Wraps a WSGI app and handles uncaught exceptions and defined exception and outputs a the exception in a
    structured format.
    Parameters:
    - wsgi_app is the app.wsgi_app of flask,
    - app_name should in correct format e.g. APP_NAME_1,
    - app_logger is the logger object"""

    def wrapper(environ, start_response):
        try:
            return wsgi_app(environ, start_response)
        except RootException as e:
            status = e.status_code
            code = e.app_err_code.upper()
            error_message = e.error_message
            additional_info = e.additional_info
            log_request_data(app_logger)
        except Exception:
            status = 500
            code = '{}_FATAL_000'.format(app_name.upper())
            error_message = 'Unknown System Error'
            stack_trace = traceback.format_exc()
            additional_info = stack_trace.splitlines()[-1]
            log_request_data(app_logger)

        response = create_json_error_response(status, code, error_message, additional_info, app_logger)
        return response(environ, start_response)
    return wrapper


def create_identifier():
    return uuid.uuid1().get_hex()


def log_error(error_details, app_logger):
    trace = traceback.format_exc()
    error_details['trace_stack'] = trace
    app_logger.error(error_details)


def construct_error_info(code, error_message, additional_info):
    logref = create_identifier()
    return {"app_err_code": code, 'logref': logref, "error_message": error_message, "additional_info": additional_info}


def create_json_error_response(status, code, error_message, additional_info, app_logger):
    error_details = construct_error_info(code, error_message, additional_info)
    _response = Response(json.dumps(error_details), status=status, content_type='application/json')
    log_error(error_details, app_logger)
    return _response


def log_request_data(app_logger):
    try:
        app_logger.info(u"Request data given to application:\n {}".format(request.data))
    except StandardError:
        app_logger.debug(u"Could not log request data")




