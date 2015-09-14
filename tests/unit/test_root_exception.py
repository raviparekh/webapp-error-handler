from logging import ERROR, CRITICAL, WARN
from unittest import TestCase
from app_error_handler.root_exception import RootException
from tests.unit.test_data import ERROR_MESSSAGES, FATAL_MESSAGES, WARNING_MESSSAGES


class TestMessages(TestCase):
    def test_should_return_valid_message_object(self):
        actual = RootException('FATAL_000', WARNING_MESSSAGES, ERROR_MESSSAGES, FATAL_MESSAGES, 500)
        self.assertEqual('FATAL_000', actual.app_err_code)
        self.assertEqual(500, actual.status_code)

    def test_should_return_valid_templated_message_object(self):
        actual = RootException('ERR_002', WARNING_MESSSAGES, ERROR_MESSSAGES, FATAL_MESSAGES, 500,
                               href='http://someUrl', error_info='some_error_info')
        self.assertEqual('ERR_002', actual.app_err_code)
        self.assertEqual(500, actual.status_code)
        self.assertTrue(actual.error_message.find('$href') == -1)

    def test_should_not_error_if_app_error_code_not_found_in_mapping(self):
        actual = RootException('Mistaken_app_error_code', WARNING_MESSSAGES, ERROR_MESSSAGES, FATAL_MESSAGES, 500,
                               href='http://someUrl', error_info='some_error_info')

        self.assertIn("**FlaskErrorHandler", actual.error_message)

    def test_log_level_is_set_correctly_when_warning_found(self):
        actual = RootException('WARN_001', WARNING_MESSSAGES, ERROR_MESSSAGES, FATAL_MESSAGES, 500)
        self.assertEqual(WARN, actual.log_level)

    def test_log_level_is_set_correctly_when_error_found(self):
        actual = RootException('ERR_001', WARNING_MESSSAGES, ERROR_MESSSAGES, FATAL_MESSAGES, 500)
        self.assertEqual(ERROR, actual.log_level)

    def test_log_level_is_set_correctly_when_fatal_found(self):
        actual = RootException('FATAL_001', WARNING_MESSSAGES, ERROR_MESSSAGES, FATAL_MESSAGES, 500)
        self.assertEqual(CRITICAL, actual.log_level)

    def test_log_level_is_set_critical_when_unknown_error_code_used(self):
        actual = RootException('Mistaken_app_error_code', WARNING_MESSSAGES, ERROR_MESSSAGES, FATAL_MESSAGES, 500)
        self.assertEqual(CRITICAL, actual.log_level)
