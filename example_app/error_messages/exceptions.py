from app_error_handler.root_exception import RootException

error_message_mapping = {'ERR_001': 'Authorisation error, incorrect login details for $user'}
fatal_error_message_mapping = {'FATAL_001': 'Constant connection error to database'}
warning_error_message_mapping = {"WARN_001": "Some warning"}


class AppRootException(RootException):

    def __init__(self, application_error_code, status_code, **kwargs):
        super(AppRootException, self).__init__(application_error_code, warning_error_message_mapping,
                                               error_message_mapping, fatal_error_message_mapping, status_code,
                                               **kwargs)


class Unauthorised(AppRootException):
    pass

