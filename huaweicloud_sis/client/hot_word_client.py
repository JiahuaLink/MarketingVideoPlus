# -*- coding: utf-8 -*-

from huaweicloud_sis.bean.hot_word_request import HotWordRequest
from huaweicloud_sis.bean.sis_config import SisConfig
from huaweicloud_sis.utils.logger_utils import logger
from huaweicloud_sis.auth import aksk_service
from huaweicloud_sis.exception.exceptions import ClientException, ServerException
import json


class HotWordClient:
    """ 热词client，可用于创建热词表、更新热词表、查询热词表列表、查询热词表、删除热词表 """
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

    def create(self, request):
        """
            创建热词表
        :param request: 热词表请求
        :return: 热词表id
        """
        if not isinstance(request, HotWordRequest):
            logger.error('the parameter in \'create_hot_word(request)\' should be HotWordRequest class')
            raise ClientException('the parameter in \'create_hot_word(request)\' should be HotWordRequest class')
        url = self._service_endpoint + '/v1/' + self._project_id + '/asr/vocabularies'
        params = request.construct_params()
        result = aksk_service.aksk_connect(self._ak, self._sk, url, params, 'POST', self._sis_config)
        return result

    def update(self, request, vocabulary_id):
        """
            更新热词表
        :param request: 热词表请求
        :param vocabulary_id: 热词表id，更新时一定要保证该热词表存在
        :return: 热词表id
        """
        if not isinstance(request, HotWordRequest):
            logger.error('the parameter in \'update_hot_word(request)\' should be HotWordRequest class')
            raise ClientException('the parameter in \'update_hot_word(request)\' should be HotWordRequest class')
        url = self._service_endpoint + '/v1/' + self._project_id + '/asr/vocabularies/' + vocabulary_id
        params = request.construct_params()
        result = aksk_service.aksk_connect(self._ak, self._sk, url, params, 'PUT', self._sis_config)
        return result

    def query_list(self):
        """
            查询热词表列表信息
        :return: 热词表列表信息
        """
        url = self._service_endpoint + '/v1/' + self._project_id + '/asr/vocabularies'
        result = aksk_service.aksk_connect(self._ak, self._sk, url, None, 'GET', self._sis_config)
        return result

    def query_by_vocabulary_id(self, vocabulary_id):
        """
            根据vocabulary_id查询热词表信息
        :param vocabulary_id: 热词表id，使用前一定要保证其已存在。
        :return:  热词表信息
        """
        url = self._service_endpoint + '/v1/' + self._project_id + '/asr/vocabularies/' + vocabulary_id
        result = aksk_service.aksk_connect(self._ak, self._sk, url, None, 'GET', self._sis_config)
        return result

    def delete(self, vocabulary_id):
        """
            根据vocabulary_id删除指定的热词表
        :param vocabulary_id: 热词表id，使用前一定要保证其已存在。
        :return: 正常删除返回结果为空，出现错误则返回error_code和error_msg
        """
        url = self._service_endpoint + '/v1/' + self._project_id + '/asr/vocabularies/' + vocabulary_id
        result = aksk_service.aksk_connect(self._ak, self._sk, url, None, 'DELETE', self._sis_config)
        if result is None:
            return result
        result_text = result.text
        return json.loads(result_text)
