# -*- coding: utf-8 -*-


class TtsRequest:
    """ 语音合成请求，除了初始化必选参数外，其他参数均可不配置使用默认 """
    def __init__(self, text):
        """
            语音合成请求初始化
        :param text: 需要合成的文本
        """
        self._text = text
        self._voice_name = 'xiaoyan'
        self._volume = 0
        self._sample_rate = '8k'
        self._speech_speed = 0
        self._pitch_rate = 0
        self._saved = False
        self._saved_path = ''

    def set_voice_name(self, voice_name):
        self._voice_name = voice_name

    def set_volume(self, volume):
        self._volume = volume

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def set_speech_speed(self, speech_speed):
        self._speech_speed = speech_speed

    def set_pitch_rate(self, picth_rate):
        self._pitch_rate = picth_rate

    def set_saved(self, saved):
        self._saved = saved

    def set_saved_path(self, saved_path):
        self._saved_path = saved_path

    def get_saved(self):
        return self._saved

    def get_saved_path(self):
        return self._saved_path

    def construct_params(self):
        params = dict()
        params['text'] = self._text
        params['voice_name'] = self._voice_name
        params['volume'] = self._volume
        params['sample_rate'] = self._sample_rate
        params['speech_speed'] = self._speech_speed
        params['pitch_rate'] = self._pitch_rate
        return params


class TtsCustomRequest:
    """ 定制语义识别请求，除了初始化必选参数外，其他参数均可不配置使用默认 """
    def __init__(self, text):
        """
            定制语音识别请求初始化
        :param text: 需要合成的文本
        """
        self._text = text
        self._audio_format = 'wav'
        self._property = 'chinese_xiaoyan_common'
        self._sample_rate = '8000'
        self._speed = 0
        self._pitch = 0
        self._volume = 50
        self._saved = False
        self._saved_path = ''

    def set_audio_format(self, audio_format):
        self._audio_format = audio_format

    def set_volume(self, volume):
        self._volume = volume

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def set_property(self, model_property):
        self._property = model_property

    def set_pitch(self, pitch):
        self._pitch = pitch

    def set_speed(self, speed):
        self._speed = speed

    def set_saved(self, saved):
        self._saved = saved

    def set_saved_path(self, saved_path):
        self._saved_path = saved_path

    def get_saved(self):
        return self._saved

    def get_saved_path(self):
        return self._saved_path

    def construct_params(self):
        config = dict()
        config['audio_format'] = self._audio_format
        config['sample_rate'] = self._sample_rate
        config['property'] = self._property
        config['speed'] = self._speed
        config['pitch'] = self._pitch
        config['volume'] = self._volume

        params = dict()
        params['text'] = self._text
        params['config'] = config
        return params
