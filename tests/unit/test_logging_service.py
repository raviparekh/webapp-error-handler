from logging import WARN, CRITICAL
import unittest
from mock import Mock
from flask_error_handler.logging_service import LoggingService


class TestLoggingService(unittest.TestCase):

    def setUp(self):
        self.mock_logger = Mock()
        self.logging_service = LoggingService("Test_app", self.mock_logger)
        self.error_details_dict = {u'trace_stack': u'None', u'error_message': u'some_error_details',
                              u'app_err_code': u'some_app_err_code', u'additional_info': u'some_additional_info',
                              u'logref': u'some_logref'}

    def test_log_error_adds_stack_trace_before_logging(self):
        mock_exception = Mock()
        mock_exception.log_level.return_value = CRITICAL
        self.logging_service.update_with_exception_data(mock_exception, Mock(), "some stack trace")

        self.logging_service.log_error(self.error_details_dict)

        self.mock_logger.critical.assert_called_once_with(self.error_details_dict)
        self.assertTrue("trace_stack" in self.error_details_dict.keys())

    def test_log_request_logs_correct_log_level(self):
        mock_exception = Mock()
        mock_exception.log_level.return_value = WARN
        self.logging_service.update_with_exception_data(mock_exception, Mock(), "some stack trace")
        self.logging_service.log_error(self.error_details_dict)
        self.mock_logger.warning.assert_called()

    def test_log_request_logs_at_critical_when_cannot_determine_log_level(self):
        mock_exception = Mock()
        mock_exception.log_level.return_value = "Unknown log level"
        self.logging_service.update_with_exception_data(mock_exception, Mock(), "some stack trace")
        self.logging_service.log_error(self.error_details_dict)
        self.mock_logger.critical.assert_called()

    def test_log_request_data_handles_exception_when_request_data_not_available(self):
        mock_request = Mock()
        mock_request.mock_request.return_value = AttributeError
        self.logging_service.update_with_exception_data(Mock(), mock_request, "some stack trace")
        self.logging_service.log_request_data()
        self.mock_logger.debug.assert_called()

    def test_create_identifier(self):
        uuid = self.logging_service.create_identifier()
        self.assertTrue(isinstance(uuid, str))