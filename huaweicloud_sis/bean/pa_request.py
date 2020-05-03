class PaAudioRequest:
    """ 语音评测请求 """

    def __init__(self, audio_data, audio_format, ref_text):
        """
            语音请求初始化
        :param audio_data: 音频 base64编码
        :param audio_format: 音频格式
        :param ref_text:  音频对应文本，用于发音评分
        """
        self._audio_data = audio_data
        self._audio_format = audio_format
        self._ref_text = ref_text
        self._language = 'en_gb'
        self._mode = 'word'

    def set_language(self, language):
        self._language = language

    def get_language(self):
        return self._language

    def set_mode(self, mode):
        self._mode = mode

    def get_mode(self):
        return self._mode

    def construct_params(self):
        params_dict = {
            'audio_data': self._audio_data,
            'ref_text': self._ref_text,
            'config': {
                'audio_format': self._audio_format,
                'language': self._language,
                'mode': self._mode
            }
        }
        return params_dict


class PaVideoRequest:
    def __init__(self, video_data, video_format, audio_data, audio_format, ref_text):
        """
            多模态评测请求
        :param video_data: 视频base64编码
        :param video_format: 视频格式
        :param audio_data: 音频 base64编码
        :param audio_format: 音频格式
        :param ref_text:  音频对应文本，用于发音评分
        """
        self._video_data = video_data
        self._video_format = video_format
        self._audio_data = audio_data
        self._audio_format = audio_format
        self._ref_text = ref_text
        self._language = 'en_gb'
        self._mode = 'word'

    def set_language(self, language):
        self._language = language

    def get_language(self):
        return self._language

    def set_mode(self, mode):
        self._mode = mode

    def get_mode(self):
        return self._mode

    def construct_parameter(self):
        params_dict = {
            'video_data': self._video_data,
            'audio_data': self._audio_data,
            'ref_text': self._ref_text,
            'config': {
                'video_format': self._video_format,
                'audio_format': self._audio_format,
                'language': self._language,
                'mode': self._mode
            }
        }
        return params_dict
