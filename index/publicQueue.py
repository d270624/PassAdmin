# -*- coding:utf-8 -*-
from queue import Queue as general


class generals:
    """# 1.将所有需要执行的列表放到队列中
       # 2.取出队列中的数据进行执行
       # 3.将队列执行的结果放到日志队列中
       # 4.取出日志队列"""

    def __init__(self):
        self.allQueue = general()
        self.logQueue = general()
        self.log = []
        self.temp = {}

    def put(self, data):
        """参数1：字典格式数据"""
        self.allQueue.put(data)  # 1.将所有需要执行的列表放到队列中

    def run(self, handlerName, methodName, operation=None):
        """参数1：handlerName 格式：类名
           参数2：methodName 格式：字符串格式，类方法名
        """
        while True:
            host = self.allQueue.get()  # 2.1 取出队列中的数据
            result = handlerName(host)  # 2.2 执行,类初始化
            result = eval("result." + methodName + "()")  # 2.3 执行提供的方法名
            if operation:
                exec(operation)  # 处理额外添加的程序，将执行结果存放在self.temp中
                if self.temp:
                    self.logQueue.put(self.temp)  # 3.将结果放到日志队列中
            else:
                if result:
                    self.logQueue.put(result)
            self.allQueue.task_done()

    def get_log(self):
        """返回methodName执行结果的日志"""
        while True:
            result = self.logQueue.get()
            self.log.append(result)
            self.logQueue.task_done()
