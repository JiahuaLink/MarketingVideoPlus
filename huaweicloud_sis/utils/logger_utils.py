import logging.handlers
import os

# 获取一个日志logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - [%(message)s]'
)
# 设置handler
root_dir = os.path.abspath('.')
logpath = os.path.join(root_dir,'huaweicloud_sis' ,"log.log")
file_handler = logging.handlers.RotatingFileHandler(logpath, maxBytes=1024*1024,
                                                    backupCount=5, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] - [%(levelname)s] - [%(message)s]'))

# 添加file_handler
logger = logging.getLogger('huaweicloud_sis')
logger.addHandler(file_handler)
