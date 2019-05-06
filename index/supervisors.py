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

    def restart(self, name):
        try:
            self.server.supervisor.stopProcess(name)
        except xmlrpc.client.Fault:
            self.server.supervisor.startProcess(name)
        try:
            self.server.supervisor.startProcess(name)
        except xmlrpc.client.Fault:
            pass

    def start_all(self):
        try:
            self.server.supervisor.startAllProcesses()
            return True
        except xmlrpc.client.Fault:
            return False

    def stop_all(self):
        try:
            self.server.supervisor.stopAllProcesses()
        except xmlrpc.client.Fault:
            return False

    def restart_all(self):
        try:
            self.server.supervisor.restart()
            return True
        except xmlrpc.client.Fault:
            return False

    def getAllProcessInfo(self):
        return self.server.supervisor.getAllProcessInfo()

    def reloadConfig(self):
        try:
            self.server.supervisor.reloadConfig()
            return True
        except xmlrpc.client.Fault:
            return False
