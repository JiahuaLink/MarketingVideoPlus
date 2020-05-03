# -*- coding: utf-8 -*-

import base64
import os
from huaweicloud_sis.utils.logger_utils import logger
from huaweicloud_sis.exception.exceptions import ClientException


def encode_file(file_path):
    if not os.path.exists(file_path):
        logger.error('The Path %s doesn\'t exist' % file_path)
        raise ClientException('The Path %s doesn\'t exist' % file_path)
    with open(file_path, 'rb') as f:
        data = f.read()
        base64_data = str(base64.b64encode(data), 'utf-8')
        return base64_data


def save_audio_from_base64str(base64_str, save_path):
    parent_path = os.path.dirname(save_path)
    if parent_path != '' and not os.path.exists(parent_path):
        os.makedirs(parent_path)
    with open(save_path, 'wb') as f:
        base64_data = base64.b64decode(base64_str)
        f.write(base64_data)
