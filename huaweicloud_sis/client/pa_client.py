from huaweicloud_sis.auth import aksk_service
from huaweicloud_sis.bean.pa_request import PaAudioRequest
from huaweicloud_sis.bean.pa_request import PaVideoRequest
from huaweicloud_sis.utils.logger_utils import logger
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.bean.sis_config import SisConfig


class PaClient:
    """ 口语评测 client """

    def __init__(self, ak, sk, region, project_id, service_endpoint=None, sis_config=None):
        """
            口语评测client初始化
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

    def assessment_audio(self, request):
        """
            语音评测接口
        :param request: 语音评测请求
        :return: 响应结果，返回为json格式
        """
        if not isinstance(request, PaAudioRequest):
            error_msg = 'the parameter in \'assessment_audio(request)\' should be PaAudioRequest class'
            logger.error(error_msg)
            raise ClientException(error_msg)
        url = self._service_endpoint + '/v1/' + self._project_id + '/assessment/audio'
        params = request.construct_params()
        result = aksk_service.aksk_connect(self._ak, self._sk, url, params, 'POST', self._sis_config)
        return result

    def assessment_video(self, request):
        """
            多模态评测接口
        :param request: 多模态评测请求
        :return: 响应结果，返回为json格式
        """
        if not isinstance(request, PaVideoRequest):
            error_msg = 'the parameter in \'assessment_video(request)\' should be PaVideoRequest class'
            logger.error(error_msg)
            raise ClientException(error_msg)
        url = self._service_endpoint + '/v1/' + self._project_id + '/assessment/video'
        params = request.construct_parameter()
        result = aksk_service.aksk_connect(self._ak, self._sk, url, params, 'POST', self._sis_config)
        return result
