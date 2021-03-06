import json
from unittest import TestCase
from mock import Mock, patch
from werkzeug.wrappers import Response
from app_error_handler.application_error_handler import register_app_for_error_handling
from app_error_handler.interfaces.logging_service_interface import LoggingServiceInterface
from app_error_handler.root_exception import RootException
from tests.unit.test_data import ERROR_MESSSAGES, FATAL_MESSAGES, WARNING_MESSSAGES


class TestAppErrorHandler(TestCase):

    def setUp(self):
        self.request_patch = patch("app_error_handler.application_error_handler.Request")
        self.request_patch.start()
        self.app = Mock()
        self.app_logger = Mock()
        self.wrapped_app = register_app_for_error_handling(self.app, 'TEST_APP', self.app_logger)
        self.dummy_environ = {'REQUEST_METHOD': 'GET'}
        self.dummy_start_response = self.record_status_code

    def tearDown(self):
        self.request_patch.stop()

    def test_handle_errors_for_unexpected_errors(self):
        self.app.side_effect = Exception
        actual_response = Response(self.wrapped_app(self.dummy_environ, self.dummy_start_response))
        self.app_logger.critical.assert_called()
        self.assertEqual(self.status_code, "500 INTERNAL SERVER ERROR")
        self.assert_response_with_expectation(u"TEST_APP_FATAL_000", u"Unknown System Error",  None, actual_response)

    def test_handle_errors_for_known_errors(self):
        self.app.side_effect = TestSomeError(u"FATAL_002", status_code=500, href=u"http://somehref")
        actual_response = Response(self.wrapped_app(self.dummy_environ, self.dummy_start_response))
        self.app_logger.critical.assert_called()
        self.assertEqual(self.status_code, "500 INTERNAL SERVER ERROR")
        self.assert_response_with_expectation(u"TEST_APP_FATAL_002", u"Unable to connect to http://somehref", None,
                                              actual_response)

    def test_custom_logging_service_is_used_when_stated(self):
        custom_logging_service = CustomLoggingService()
        app = Mock()
        app.side_effect = Exception
        wrapped_app = register_app_for_error_handling(app, 'TEST_APP', self.app_logger,
                                                      custom_logging_service=custom_logging_service)
        wrapped_app(self.dummy_environ, self.dummy_start_response)
        self.assertEqual(1, custom_logging_service.log_error_calls)

    def test_custom_logging_service_is_not_used_when_not_stated(self):
        custom_logging_service = CustomLoggingService()
        app = Mock()
        app.side_effect = Exception
        wrapped_app = register_app_for_error_handling(app, 'TEST_APP', self.app_logger)
        wrapped_app(self.dummy_environ, self.dummy_start_response)
        self.assertEqual(0, custom_logging_service.log_error_calls)

    def assert_response_with_expectation(self, app_err_code, expected_error_message, additional_info, actual_response):
        actual_json = json.loads(actual_response.data.decode("utf-8"))
        expected_response = {u'error_message': expected_error_message, u'app_err_code': app_err_code,
                             u'additional_info': additional_info}
        self.assertIsNotNone(actual_json.pop("logref"))
        self.assertDictEqual(expected_response, actual_json)

    def record_status_code(self, status_code, headers):
        self.status_code = status_code
        self.headers = headers


class TestAppRootError(RootException):
    def __init__(self, app_err_code, status_code=500, **kwargs):
        super(TestAppRootError, self).__init__(app_err_code, WARNING_MESSSAGES, ERROR_MESSSAGES, FATAL_MESSAGES,
                                               status_code, **kwargs)


class TestSomeError(TestAppRootError):
    def __init__(self, app_err_code, status_code=500, **kwargs):
        super(TestSomeError, self).__init__(app_err_code, status_code, **kwargs)


class CustomLoggingService(LoggingServiceInterface):

    def __init__(self):
        self.log_error_calls = 0

    def log_error(self, log_level_fn, error_details, request, stack_trace):
        self.log_error_calls += 1