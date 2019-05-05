from xmlrpc.client import ServerProxy
import xmlrpc


class superv:
    def __init__(self, ip, user, password, port=9001):
        self.server = ServerProxy('http://' + user + ':' + password + '@' + ip + ':' + str(port) + '/RPC2')

    def start(self, name):
        try:
            self.server.supervisor.startProcess(name)
            return True
        except xmlrpc.client.Fault:
            return False

    def stop(self, name):
        try:
            self.server.supervisor.stopProcess(name)
            return True
        except xmlrpc.client.Fault:
            return False

    def restart_all(self, name):
        try:
            self.server.supervisor.restart()
            return True
        except xmlrpc.client.Fault:
            return False

    def restart(self, name):
        try:
            self.server.supervisor.stopProcess(name)
        except xmlrpc.client.Fault:
            self.server.supervisor.startProcess(name)
        try:
            self.server.supervisor.startProcess(name)
        except xmlrpc.client.Fault:
            pass

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
