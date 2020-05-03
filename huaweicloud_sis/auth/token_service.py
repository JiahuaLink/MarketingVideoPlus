# -*- coding: utf-8 -*-

from huaweicloud_sis.utils import http_utils
from huaweicloud_sis.bean.sis_config import SisConfig
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.utils.logger_utils import logger


def get_token(user_name, password, domain_name, region, url=None, config=SisConfig()):
    """
        获取token
    :param user_name:   用户名
    :param password:    密码
    :param domain_name: 账户名，一般等同用户名
    :param region:      区域，如cn-north-4
    :param url:         请求token的url，可使用默认值
    :param config       配置信息
    :return:            请求的token
    """
    if url is None:
        url = 'https://iam.' + region + '.myhuaweicloud.com/v3/auth/tokens'
    if not isinstance(config, SisConfig):
        error_msg = 'the param \'config\' in token_service must be SisConfig class'
        logger.error(error_msg)
        raise ClientException(error_msg)
    time_out = (config.get_connect_timeout(), config.get_read_timeout())
    proxy = config.get_proxy()
    auth_data = {
        "auth": {
            "identity": {
                "password": {
                    "user": {
                        "name": user_name,
                        "password": password,
                        "domain": {
                            "name": domain_name
                        }
                    }
                },
                "methods": [
                    "password"
                ]
            },
            "scope": {
                "project": {
                    "name": region
                }
            }
        }
    }

    headers = {'Content-Type': 'application/json'}
    req = http_utils.http_connect(url, headers, auth_data, 'POST', time_out, proxy)
    if 'X-Subject-Token' not in req.headers:
        logger.error('Error occurs in getting token, %s' % req.text)
        raise ClientException('Error occurs in getting token, %s' % req.text)
    token = req.headers['X-Subject-Token']
    return token
