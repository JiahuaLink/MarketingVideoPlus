# -*- coding: utf-8 -*-


class RasrRequest:
    """ 实时语音转写请求，除了初始化必选参数外，其他参数均可不配置使用默认 """
    def __init__(self, audio_format, model_property):
        """
            实时语音转写请求初始化
        :param audio_format:   音频格式，详见api文档
        :param model_property: 属性字符串，language_sampleRate_domain, 如chinese_8k_common，详见api文档
        """
        self._audio_format = audio_format
        self._property = model_property
        self._add_punc = 'no'
        self._vad_head = 10000
        self._vad_tail = 500
        self._max_seconds = 30
        self._interim_results = 'no'
        self._vocabulary_id = None

    def set_add_punc(self, add_punc):
        self._add_punc = add_punc

    def set_vad_head(self, vad_head):
        self._vad_head = vad_head

    def set_vad_tail(self, vad_tail):
        self._vad_tail = vad_tail

    def set_max_seconds(self, max_seconds):
        self._max_seconds = max_seconds

    def set_interim_results(self, interim_results):
        self._interim_results = interim_results

    def set_vocabulary_id(self, vocabulary_id):
        self._vocabulary_id = vocabulary_id

    def construct_params(self):
        config = dict()
        config['audio_format'] = self._audio_format
        config['property'] = self._property
        config['add_punc'] = self._add_punc
        config['vad_head'] = self._vad_head
        config['vad_tail'] = self._vad_tail
        config['max_seconds'] = self._max_seconds
        config['interim_results'] = self._interim_results
        if self._vocabulary_id is not None:
            config['vocabulary_id'] = self._vocabulary_id

        params = dict()
        params['command'] = 'START'
        params['config'] = config
        return params
