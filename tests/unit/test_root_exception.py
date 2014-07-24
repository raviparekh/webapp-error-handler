from unittest import TestCase
from flask_error_handler.root_exception import RootException
from tests.unit.test_data import ERROR_MESSSAGES, FATAL_MESSAGES


class TestMessages(TestCase):
    def test_should_return_valid_message_object(self):
        actual = RootException('TEST_APP_FATAL_000', ERROR_MESSSAGES, FATAL_MESSAGES, 500)
        self.assertEqual('TEST_APP_FATAL_000', actual.app_err_code)
        self.assertEqual(500, actual.status_code)

    def test_should_return_valid_templated_message_object(self):
        actual = RootException('TEST_APP_ERR_002', ERROR_MESSSAGES, FATAL_MESSAGES, 500,
                               href='http://someUrl', error_info='some_error_info')
        self.assertEqual('TEST_APP_ERR_002', actual.app_err_code)
        self.assertEqual(500, actual.status_code)
        self.assertTrue(actual.error_message.find('$href') == -1)

    def test_should_not_error_if_app_error_code_not_found_in_mapping(self):
        actual = RootException('Mistaken_app_error_code', ERROR_MESSSAGES, FATAL_MESSAGES, 500,
                               href='http://someUrl', error_info='some_error_info')
        self.assertEquals("**PyErrorHandler - Unable to find error code 'Mistaken_app_error_code' "
                          "in provided error code mapping",
                          actual.error_message)
