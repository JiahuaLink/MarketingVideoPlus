# -*- coding: utf-8 -*-


class SisConfig:
    """ client配置参数，包括超时、代理 """
    def __init__(self):
        self.connect_timeout = 10
        self.read_timeout = 10
        self.connect_lost_timeout = 4
        self.proxy = None

    def set_connect_timeout(self, timeout):
        """
            设置连接超时
        :param timeout: seconds
        """
        self.connect_timeout = timeout

    def get_connect_timeout(self):
        """
            返回连接超时时间
        :return: connect_timeout, 单位秒
        """
        return self.connect_timeout

    def set_read_timeout(self, timeout):
        """
            设置读取超时
        :param timeout: seconds
        """
        self.read_timeout = timeout

    def get_read_timeout(self):
        """
            返回读取超时
        :return: read_timeout, 单位秒
        """
        return self.read_timeout

    def set_proxy(self, proxy):
        """
            设置代理
        :param proxy: 格式为list，[host, port] 或 [host, port, username, password]
        """
        self.proxy = proxy

    def get_proxy(self):
        """
            返回代理
        :return: proxy
        """
        return self.proxy

    def set_connect_lost_timeout(self, timeout):
        """
            设置connect lost 超时, 在并发满足要求下不需要设置此参数
        :param timeout: seconds
        """
        self.connect_lost_timeout = timeout

    def get_connect_lost_timeout(self):
        """
            返回connnect lost超时
        :return: connect_lost_timeout, 单位秒
        """
        return self.connect_lost_timeout
