from xmlrpc.client import ServerProxy
import xmlrpc


class superv:
    def __init__(self, ip, user, password, port=9001):
        self.server = ServerProxy('http://' + user + ':' + password + '@' + ip + ':' + str(port) + '/RPC2')

    def tailf(self, name):
        result = self.server.supervisor.tailProcessLog(name, 0, 1024)
        tmp_var = result[1]
        print(result[0], end='')
        while True:
            current = self.server.supervisor.tailProcessLog(name, 0, 0)  # 1005
            if current[1] != tmp_var:
                result = self.server.supervisor.tailProcessLog(name, 0, current[1] - tmp_var)
                print(result[0], end='')
                tmp_var = current[1]

    def start(self, name):
        try:
            self.server.supervisor.startProcess(name)
            print('启动成功')
        except xmlrpc.client.Fault:
            print('启动失败')

    def stop(self, name):
        try:
            self.server.supervisor.stopProcess(name)
            print('停止成功')
        except xmlrpc.client.Fault:
            print('进程未运行')

    def restart_all(self, name):
        try:
            self.server.supervisor.restart()
            print('重启成功')
        except xmlrpc.client.Fault:
            print('重启失败')

    def restart(self, name):
        try:
            self.server.supervisor.stopProcess(name)
        except:
            pass
        try:
            self.server.supervisor.stopProcess(name)
            print('重启成功')
        except:
            print('重启失败')

    def state(self, name):
        res = self.server.supervisor.getProcessInfo(name)
        methods = self.server.system.listMethods()
        print(methods)

    def start_all(self):
        self.server.supervisor.startAllProcesses()

    def stop_all(self):
        self.server.supervisor.stopAllProcesses()

    def getAllProcessInfo(self):
        return self.server.supervisor.getAllProcessInfo()

    def tools(self):
        self.server.system.listMethods()
