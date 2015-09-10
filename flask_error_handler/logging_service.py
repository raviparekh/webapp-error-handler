import json
from logging import WARN, CRITICAL, ERROR
import uuid
from werkzeug.wrappers import Response


class LoggingService(object):

    def __init__(self, app_name, app_logger):
        self.e = None
        self.stack_trace = None
        self.request = None
        self.app_logger = app_logger
        self.app_name = app_name
        self._logging_level_fn = {WARN: self.app_logger.warning, ERROR: self.app_logger.error,
                                  CRITICAL: self.app_logger.critical}

    def update_with_exception_data(self, exception_obj, app_request, stack_trace):
        self.e = exception_obj
        self.request = app_request
        self.stack_trace = stack_trace

    @staticmethod
    def create_identifier():
        return uuid.uuid1().hex

    def log_error(self, error_details):
        self.log_request_data()
        error_details['trace_stack'] = self.stack_trace
        fn = self._logging_level_fn.get(self.e.log_level, self.app_logger.critical)
        fn(error_details)

    def construct_error_info(self, code, error_message, additional_info):
        log_id = self.create_identifier()
        return {"app_err_code": (self.app_name + "_" + code).upper(), "logref": log_id,
                "error_message": error_message, "additional_info": additional_info}

    def create_json_error_response(self):
        error_details = self.construct_error_info(self.e.app_err_code, self.e.error_message, self.e.additional_info)
        _response = Response(json.dumps(error_details), status=self.e.status_code, content_type='application/json')
        self.log_error(error_details)
        return _response

    def log_request_data(self):
        try:
            self.app_logger.info(u"Request data given to application:\n {}".format(self.request.data))
        except (AttributeError, RuntimeError) as e:
            self.app_logger.debug(u"Could not log request data. Error info: {}".format(e))
