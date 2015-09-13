import unittest
from mock import Mock
from flask_error_handler.exception_handling_service import ExceptionHandler


class TestExceptionHandler(unittest.TestCase):

    def setUp(self):
        self.mock_logging_service = Mock()
        self.log_request_data_count = 0
        self.mock_exception = Mock()
        self.mock_exception.app_err_code = u'some_app_err_code'
        self.mock_exception.error_message = u'some_error_details'
        self.mock_exception.additional_info = u'some_additional_info'
        self.mock_exception.status_code = 200
        self.exception_manager = ExceptionHandler("Test_app", self.mock_logging_service)

    def test_construct_error_details_creates_error_details_correctly(self):
        self.exception_manager.update_with_exception_data(self.mock_exception, Mock(), None)
        expected = {u'error_message': u'some_error_details',
                                   u'additional_info': u'some_additional_info'}

        actual = self.exception_manager.construct_error_details()
        self.assertIsNotNone(actual.pop('logref', None))
        self.assertEqual(actual.pop('app_err_code'), 'TEST_APP_SOME_APP_ERR_CODE')
        self.assertDictEqual(expected, actual)

    def test_get_http_status_code(self):
        self.exception_manager.update_with_exception_data(self.mock_exception, Mock(), None)
        self.assertEqual(200, self.exception_manager.get_http_status_code())

    def test_create_identifier(self):
        uuid = self.exception_manager._create_exception_identifier()
        self.assertTrue(isinstance(uuid, str))
