import json
from unittest import TestCase
from mock import Mock, patch
from flask_error_handler.app_error_handler import flask_application_error_wrapper, create_json_error_response, \
    log_request_data, log_error
from flask_error_handler.root_exception import RootException
from tests.unit.test_data import ERROR_MESSSAGES, FATAL_MESSAGES

class TestAppErrorHandler(TestCase):

    def setUp(self):
        self.app = Mock()
        self.app_logger = Mock()
        self.wrapped_app = flask_application_error_wrapper(self.app, 'TEST_APP', self.app_logger)
        self.dummy_environ = {'REQUEST_METHOD': 'GET'}
        self.dummy_start_response = Mock()

    @patch('flask_error_handler.app_error_handler.create_json_error_response')
    @patch('flask_error_handler.app_error_handler.log_error')
    def test_handle_errors_for_unexpected_errors(self, mock_log_error, mock_create_json_error_response):
        self.app.side_effect = Exception
        mock_create_json_error_response.return_value = Mock()
        self.wrapped_app(self.dummy_environ, self.dummy_start_response)
        mock_log_error.assert_called()
        mock_create_json_error_response.assert_called()

    @patch('flask_error_handler.app_error_handler.create_json_error_response')
    @patch('flask_error_handler.app_error_handler.log_error')
    def test_handle_errors_for_known_errors(self, mock_log_error, mock_create_json_error_response):
        self.app.side_effect = TestSomeError('TEST_APP_FATAL_000')
        self.wrapped_app(self.dummy_environ, self.dummy_start_response)
        mock_log_error.assert_called()
        mock_create_json_error_response.assert_called()

    @patch('flask_error_handler.app_error_handler.create_json_error_response')
    @patch('flask_error_handler.app_error_handler.log_error')
    def test_handle_errors_for_unknown_errors(self, mock_log_error, mock_create_json_error_response):
        self.app.side_effect = Exception
        self.wrapped_app(self.dummy_environ, self.dummy_start_response)
        mock_log_error.assert_called()
        mock_create_json_error_response.assert_called()

    def test_log_error(self):
        mock_logger = Mock()
        error_details_dict = {u'trace_stack': u'None', u'error_message': u'some_error_details',
                              u'app_err_code': u'some_app_err_code', u'additional_info': u'some_additional_info',
                              u'logref': u'some_logref'}
        log_error(error_details_dict, mock_logger)
        mock_logger.error.assert_called_once_with(error_details_dict)

    def test_log_request_data(self):
        log_request_data(self.app_logger)
        self.app_logger.info.assert_called()

    @patch('flask_error_handler.app_error_handler.create_identifier')
    def test_create_json_error_response(self, mock_create_identifier):
        mock_create_identifier.return_value = u'some_logref'
        expected = {u'error_message': u'some_error_details', u'app_err_code': u'some_app_err_code',
                    u'additional_info': u'some_additional_info', u'logref': u'some_logref'}
        app_logger = Mock()
        response = create_json_error_response(400, 'some_app_err_code', 'some_error_details', 'some_additional_info',
                                              app_logger)
        response_content = json.loads(response.data)
        self.assertEqual(expected, response_content)
        self.assertEqual(400, response.status_code)
        app_logger.error.assert_called()


class TestAppRootError(RootException):
    def __init__(self, app_err_code, status_code=500, **kwargs):
        super(TestAppRootError, self).__init__(app_err_code, ERROR_MESSSAGES, FATAL_MESSAGES, status_code, **kwargs)

class TestSomeError(TestAppRootError):
    def __init__(self, app_err_code, **kwargs):
        super(TestSomeError, self).__init__(app_err_code, 400, **kwargs)

