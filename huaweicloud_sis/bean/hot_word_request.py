from huaweicloud_sis.utils.logger_utils import logger


class HotWordRequest:
    def __init__(self, name, word_list):
        self._name = name
        self._word_list = word_list
        self._language = 'chinese_mandarin'
        self._description = ''

    def set_description(self, description):
        self._description = description

    def set_language(self, language):
        self._language = language

    def construct_params(self):
        params_dict = {
            'name': self._name,
            'language': self._language,
            'description': self._description,
            'contents': self._word_list
        }
        return params_dict
