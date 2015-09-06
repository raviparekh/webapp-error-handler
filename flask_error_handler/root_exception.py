import string


class RootException(Exception):
    def __init__(self, app_err_code, error_message_mapping, fatal_error_message_mapping, status_code=500, **kwargs):
        try:
            error_message = error_message_mapping[app_err_code]
        except KeyError:
            error_message = fatal_error_message_mapping.get(app_err_code)

        self.message = {}
        self.app_err_code = app_err_code
        self.error_message = error_message
        self.status_code = status_code
        self.additional_info = kwargs.get('additional_info')
        self._determine_message(kwargs)

    def _determine_message(self, kwargs):
        if self.error_message:
            template = string.Template(self.error_message)
            self.error_message = template.safe_substitute(**kwargs)
        else:
            self.error_message = "**FlaskErrorHandler - Unable to find error code '{}' in provided " \
                                 "error code mapping".format(self.app_err_code)

    def __str__(self):
        return u"%s: %s, status code: %s" % (self.app_err_code, self.error_message, self.status_code)

