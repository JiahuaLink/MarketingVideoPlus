# -*- coding: utf-8 -*-

from huaweicloud_sis.utils.logger_utils import logger
from huaweicloud_sis.exception.exceptions import ClientException


class AsrCustomShortRequest:
    """ 一句话识别请求，除了初始化必选参数外，其他参数均可不配置使用默认 """
    def __init__(self, audio_format, model_property, data):
        """
            一句话识别请求初始化
        :param audio_format:    音频格式，详见api文档
        :param model_property:  language_sampleRate_domain, 如chinese_8k_common, 详见api文档
        :param data:            音频转化后的base64字符串
        """
        self._audio_format = audio_format
        self._property = model_property
        self._data = data
        self._add_punc = 'no'
        self._vocabulary_id = None

    def set_add_punc(self, add_punc):
        self._add_punc = add_punc

    def set_vocabulary_id(self, vocabulary_id):
        self._vocabulary_id = vocabulary_id

    def construct_params(self):
        params = dict()
        params['data'] = self._data
        config = dict()
        config['audio_format'] = self._audio_format
        config['property'] = self._property
        config['add_punc'] = self._add_punc
        if self._vocabulary_id is not None:
            config['vocabulary_id'] = self._vocabulary_id
        params['config'] = config
        return params


class AsrCustomLongRequest:
    """ 录音文件识别请求，除了初始化必选参数外，其他参数均可不配置使用默认 """
    def __init__(self, audio_format, model_property, data_url):
        """
            录音文件识别初始化
        :param audio_format:   音频格式，详见api文档
        :param model_property: 属性字符串，language_sampleRate_domain, 详见api文档
        :param data_url:       音频的obs链接
        """
        self._audio_format = audio_format
        self._property = model_property
        self._data_url = data_url
        self._add_punc = 'no'
        self._need_analysis_info = False
        self._diarization = True
        self._channel = 'MONO'
        self._emotion = True
        self._speed = True
        self._vocabulary_id = None

    def set_add_punc(self, add_punc):
        self._add_punc = add_punc

    def set_need_analysis_info(self, need_analysis_info):
        self._need_analysis_info = need_analysis_info

    def set_diarization(self, diarization):
        self._diarization = diarization

    def set_channel(self, channel):
        self._channel = channel

    def set_emotion(self, emotion):
        self._emotion = emotion

    def set_speed(self, speed):
        self._speed = speed

    def set_vocabulary_id(self, vocabulary_id):
        self._vocabulary_id = vocabulary_id

    def construct_parameter(self):
        params = dict()
        params['data_url'] = self._data_url
        config = dict()
        config['audio_format'] = self._audio_format
        config['property'] = self._property
        config['add_punc'] = self._add_punc
        if self._need_analysis_info:
            need_analysis_info = dict()
            need_analysis_info['diarization'] = self._diarization
            need_analysis_info['channel'] = self._channel
            need_analysis_info['emotion'] = self._emotion
            need_analysis_info['speed'] = self._speed
            config['need_analysis_info'] = need_analysis_info
        if self._vocabulary_id is not None:
            config['vocabulary_id'] = self._vocabulary_id
        params['config'] = config
        return params


class AsrRequest:
    """ 短语音识别请求， data（音频Base64编码）和url（音频obs链接）参数必选二选一。"""
    def __init__(self):
        self._encode_type = 'wav'
        self._sample_rate = '8k'
        self._url = None
        self._data = None

    def set_data(self, data):
        self._data = data

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def set_url(self, url):
        self._url = url

    def set_encode_type(self, encode_type):
        self._encode_type = encode_type

    def construct_params(self):
        paras = dict()
        paras['encode_type'] = self._encode_type
        paras['sample_rate'] = self._sample_rate
        if self._data is None and self._url is None:
            logger.error('data and url can\'n be both None')
            raise ClientException('data and url can\'n be both None, you can choose set one parameter')
        if self._data is not None and self._url is not None:
            logger.warn('when data and url are not both None, only data can take effect.')
        if self._data is not None:
            paras['data'] = self._data
        else:
            paras['url'] = self._url
        return paras

