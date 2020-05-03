# -*- coding: utf-8 -*-

from huaweicloud_sis.utils.logger_utils import logger
from huaweicloud_sis.exception.exceptions import ClientException


class RasrCallBack:
    """ 实时语音转写的监听接口，监听创立链接、开始、中间响应、结束、关闭连接、错误 """
    def on_open(self):
        logger.debug('websocket connect success')

    def on_start(self, trace_id):
        logger.debug('websocket start, trace_id is %s' % trace_id)

    def on_response(self, message):
        raise ClientException('no response implementation')

    def on_end(self, trace_id):
        logger.debug('websocket end, trace_id is %s' % trace_id)

    def on_close(self):
        logger.debug('websocket close')

    def on_error(self, error):
        logger.error(error)
