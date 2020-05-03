# -*- coding: utf-8 -*-

from huaweicloud_sis.auth import aksk_service
from huaweicloud_sis.bean.asr_request import AsrRequest
from huaweicloud_sis.bean.asr_request import AsrCustomLongRequest
from huaweicloud_sis.bean.asr_request import AsrCustomShortRequest
from huaweicloud_sis.utils.logger_utils import logger
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.bean.sis_config import SisConfig


class AsrClient:
    """ 短语音识别client """
    def __init__(self, ak, sk, region, service_endpoint=None, sis_config=None):
        """
            短语音识别client初始化
        :param ak:                  用户的ak
        :param sk:                  用户的sk
        :param region:              区域，如cn-north-1
        :param service_endpoint:    终端节点，一般使用默认即可，不需要填写此值。
        :param sis_config:          配置，包括超时和代理等设置，可不填使用默认即可。
        """
        self._ak = ak
        self._sk = sk
        self._region = region
        if service_endpoint is None:
            self._service_endpoint = 'https://sis.' + region + '.myhuaweicloud.com'
        else:
            self._service_endpoint = service_endpoint
        if sis_config is None:
            self._sis_config = SisConfig()
        else:
            self._sis_config = sis_config

    def get_asr_response(self, request):
        """
            短语音识别接口
        :param request: 短语音识别请求 AsrRequest
        :return: 短语音识别响应，json格式
        """
        if not isinstance(request, AsrRequest):
            logger.error('the parameter in \'get_asr_response(request)\' should be AsrRequest class')
            raise ClientException('the parameter in \'get_asr_response(request)\' should be AsrRequest class')
        url = self._service_endpoint + '/v1.0/voice/asr/sentence'
        params = request.construct_params()
        result = aksk_service.aksk_connect(self._ak, self._sk, url, params, 'POST', self._sis_config)
        return result


class AsrCustomizationClient:
    """ 定制语音识别client """
    def __init__(self, ak, sk, region, project_id, service_endpoint=None, sis_config=None):
        """
            定制语音识别client初始化
        :param ak:                  ak
        :param sk:                  sk
        :param region:              区域，如cn-north-4
        :param project_id:          项目id，可参考https://support.huaweicloud.com/api-sis/sis_03_0008.html
        :param service_endpoint:    终端节点，可不填使用默认即可
        :param sis_config:          配置信息，包括超时、代理等，可不填使用默认即可。
        """
        self._ak = ak
        self._sk = sk
        self._region = region
        self._project_id = project_id
        if service_endpoint is None:
            self._service_endpoint = 'https://sis-ext.' + region + '.myhuaweicloud.com'
        else:
            self._service_endpoint = service_endpoint
        if sis_config is None:
            self._sis_config = SisConfig()
        else:
            self._sis_config = sis_config

    def get_short_response(self, request):
        """
            一句话识别接口
        :param request: 一句话识别请求AsrCustomShortRequest
        :return: 一句话识别响应结果，返回为json格式
        """
        if not isinstance(request, AsrCustomShortRequest):
            error_msg = 'the parameter in \'get_short_response(request)\' should be AsrCustomShortRequest class'
            logger.error(error_msg)
            raise ClientException(error_msg)
        url = self._service_endpoint + '/v1/' + self._project_id + '/asr/short-audio'
        params = request.construct_params()
        result = aksk_service.aksk_connect(self._ak, self._sk, url, params, 'POST', self._sis_config)
        return result

    def submit_job(self, request):
        """
            录音文件识别，提交任务接口
        :param request: 录音文件识别请求
        :return: job_id
        """
        if not isinstance(request, AsrCustomLongRequest):
            error_msg = 'the parameter in \'submit_job(request)\' should be AsrCustomLongRequest class'
            logger.error(error_msg)
            raise ClientException(error_msg)
        url = self._service_endpoint + '/v1/' + self._project_id + '/asr/transcriber/jobs'
        params = request.construct_parameter()
        result = aksk_service.aksk_connect(self._ak, self._sk, url, params, 'POST', self._sis_config)
        if 'job_id' not in result:
            error_msg = 'The result of long audio transcription doesn\'t contain key job_id, result is ' % result
            logger.error(error_msg)
            raise ClientException(error_msg)
        return result['job_id']

    def get_long_response(self, job_id):
        """
            录音文件识别状态查询接口
        :param job_id: job_id
        :return: 返回的结果，json格式
        """
        url = self._service_endpoint + '/v1/' + self._project_id + '/asr/transcriber/jobs/' + job_id
        result = aksk_service.aksk_connect(self._ak, self._sk, url, None, 'GET', self._sis_config)
        return result
