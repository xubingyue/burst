# -*- coding: utf-8 -*-
from collections import Counter


class StatCounter(object):

    """
    统计计算类
    """

    # 客户端连接数
    clients = 0
    # 客户端请求数
    client_req = 0
    # 客户端回应数
    client_rsp = 0
    # worker请求数
    worker_req = 0
    # worker回应数
    worker_rsp = 0
    # 作业完成时间统计
    jobs_time_counter = Counter()
    # 作业时间统计标准
    jobs_time_benchmark = None

    def __init__(self, jobs_time_benchmark):
        self.jobs_time_benchmark = jobs_time_benchmark

    def add_job_time(self, job_time):
        """
        添加一个新的时间
        :param job_time:
        :return:
        """

        def trans_to_counter_value(value):
            """
            把时间计算为一个可以统计分布的数值
            :return:
            """

            for dst_value in self.jobs_time_benchmark:
                if value < dst_value:
                    return dst_value
            else:
                return 'more'

        counter_value = trans_to_counter_value(job_time)
        self.jobs_time_counter[counter_value] += 1
