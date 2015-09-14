import json
from logging import CRITICAL, WARN, ERROR
import unittest
from mock import Mock
from app_error_handler.logging_service import LoggingService


class TestLoggingService(unittest.TestCase):

    def setUp(self):
        self.mock_logger = CustomMockLogger()
        self.logging_service = LoggingService(self.mock_logger)
        self.error_details_dict = {u'trace_stack': u'None', u'error_message': u'some_error_details',
                      u'app_err_code': u'some_app_err_code', u'additional_info': u'some_additional_info'}

    def test_log_request_data_handles_attribute_error_when_request_data_not_available(self):
        self.logging_service._log_request_data(CustomRequestMock(AttributeError))
        self.assertEqual(1, self.mock_logger.debug_calls)

    def test_log_request_data_handles_runtime_error_when_request_data_not_available(self):
        self.logging_service._log_request_data(CustomRequestMock(RuntimeError))
        self.assertEqual(1, self.mock_logger.debug_calls)

    def test_log_request_data_logs_at_info(self):
        self.logging_service._log_request_data(Mock())
        self.assertEqual(1, self.mock_logger.info_calls)

    def test_log_error_adds_stack_trace_before_logging(self):
        error_details = {u'error_message': u'some_error_details'}
        self.logging_service.log_error(ERROR, error_details, "some request", "some stack trace")
        self.assertTrue(u'trace_stack' in json.loads(self.mock_logger.data).keys())

    def test_log_error_logs_at_warn_log_level(self):
        self.logging_service.log_error(WARN, self.error_details_dict, "some request", "some stack trace")
        self.assertEqual(1, self.mock_logger.warning_calls)

    def test_log_error_logs_at_error_log_level(self):
        self.logging_service.log_error(ERROR, self.error_details_dict, "some request", "some stack trace")
        self.assertEqual(1, self.mock_logger.error_calls)

    def test_log_error_logs_at_critical_log_level(self):
        self.logging_service.log_error(CRITICAL, self.error_details_dict, "some request", "some stack trace")
        self.assertEqual(1, self.mock_logger.critical_calls)

    def test_log_request_logs_at_critical_when_cannot_determine_log_level(self):
        self.logging_service.log_error("Unknown", self.error_details_dict, "some request", "some stack trace")
        self.assertEqual(1, self.mock_logger.critical_calls)


class CustomMockLogger(object):

    def __init__(self):
        self.warning_calls = 0
        self.error_calls = 0
        self.critical_calls = 0
        self.info_calls = 0
        self.debug_calls = 0
        self.data = None

    def warning(self, data):
        self.warning_calls += 1
        self.data = data

    def error(self, data):
        self.error_calls += 1
        self.data = data

    def critical(self, data):
        self.critical_calls += 1
        self.data = data

    def info(self, data):
        self.info_calls += 1
        self.data = data

    def debug(self, data):
        self.debug_calls += 1
        self.data = data


class CustomRequestMock(object):

    def __init__(self, ex):
        self.ex = ex

    @property
    def data(self):
        raise self.ex