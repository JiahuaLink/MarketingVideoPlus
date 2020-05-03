# -*- coding: utf-8 -*-

import json
from huaweicloud_sis.auth import signer
from huaweicloud_sis.bean.sis_config import SisConfig
from huaweicloud_sis.utils import http_utils
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.utils.logger_utils import logger


def _get_signed_headers(ak, sk, url, params, http_method):
    """
        根据ak和sk以及请求信息获取加密头部
    @:return 加密的头部
    """
    scheme, host, uri = http_utils.generate_scheme_host_uri(url)
    body = params
    if isinstance(params, dict):
        body = json.dumps(params)
    kreq = signer.HttpRequest()
    kreq.scheme = scheme
    kreq.host = host
    kreq.uri = uri
    kreq.method = http_method
    kreq.headers = {'Content-Type': 'application/json'}
    if params is not None:
        kreq.body = body

    sig = signer.Signer()
    sig.Key = ak
    sig.Secret = sk
    sig.Sign(kreq)
    return kreq.headers


def aksk_connect(ak, sk, url, params, http_method, config=None):
    """
        根据url，返回json
    :param ak:  ak
    :param sk:  sk
    :param url: 完整请求url
    :param params:  请求参数， dict
    :param http_method: 请求方法，'POST' or 'GET', 其他会报错
    :param config: SisConfig(), 配置超时和代理
    :return: http返回结果转化为json
    """
    sis_config = config
    if sis_config is None:
        sis_config = SisConfig()
    if not isinstance(sis_config, SisConfig):
        error_msg = 'the param \'config\' in aksk_connect must be SisConfig class'
        logger.error(error_msg)
        raise ClientException(error_msg)
    signed_headers = _get_signed_headers(ak, sk, url, params, http_method)
    time_out = (sis_config.get_connect_timeout(), sis_config.get_read_timeout())
    resp = http_utils.http_connect(url, signed_headers, params, http_method, time_out, sis_config.get_proxy())
    json_result = http_utils.parse_resp(resp)
    if resp is not None:
        resp.close()
    return json_result
