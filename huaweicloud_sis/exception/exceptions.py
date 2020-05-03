# -*- coding: utf-8 -*-


class ClientException(Exception):
    def __init__(self, error_msg):
        super().__init__(self, error_msg)
        self._error_msg = error_msg

    def get_error_msg(self):
        return self._error_msg

    def __str__(self):
        return self.get_error_msg()


class ServerException(Exception):
    def __init__(self, error_code, error_msg):
        dict1 = dict()
        dict1['error_code'] = error_code
        dict1['error_msg'] = error_msg
        super().__init__(self, str(dict1))
        self._error_code = error_code
        self._error_msg = error_msg

    def get_error_code(self):
        return self._error_code

    def get_error_msg(self):
        return self._error_msg

    def __str__(self):
        return 'error_code: ' + self.get_error_code() + '\t' + 'error_msg: ' + self.get_error_msg()




