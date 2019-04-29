import random, string, paramiko, xlwt
# from ftplib import FTP
import telnetlib
import xlrd
import re
import os
from index.tools.channel.public import *
from queue import Queue as LinxQueue
from index.Rsa import *
import socket
import logging

mylog = logging.getLogger('django.server')


class Excel:
    def __init__(self):
        self.file = xlwt.Workbook()
        self.table = self.file.add_sheet('详细列表', cell_overwrite_ok=True)
        self.table.write(0, 0, '分类')
        self.table.write(0, 1, '服务器名')
        self.table.write(0, 2, '系统')
        self.table.write(0, 3, '外网IP')
        self.table.write(0, 4, '内网IP')
        self.table.write(0, 5, 'Root账号')
        self.table.write(0, 6, 'Root密码')
        self.table.write(0, 7, '用户')
        self.table.write(0, 8, '密码')
        self.table.write(0, 9, '端口')

    def update(self, cursor):
        en = RsaChange()
        for x, mes in enumerate(cursor, 1):
            hostname = mes.hostname
            ip = mes.ip
            intranet_ip = mes.intranet_ip
            user = mes.user
            pwd = en.decrypt(mes.password)
            normal_user = mes.normal_user
            normal_pwd = en.decrypt(mes.normal_pwd)
            port = mes.port
            user_group = str(mes.user_group)
            system = mes.get_system_display()
            self.table.write(x, 0, user_group)
            self.table.write(x, 1, hostname)
            self.table.write(x, 2, system)
            self.table.write(x, 3, ip)
            self.table.write(x, 4, intranet_ip)
            self.table.write(x, 5, user)
            self.table.write(x, 6, pwd)
            self.table.write(x, 7, normal_user)
            self.table.write(x, 8, normal_pwd)
            self.table.write(x, 9, port)

    def save(self):
        self.file.save('远程账号密码表.xls')
        # ftp = FTP()
        # ftp.set_pasv(False)
        # ftp.encoding = 'gbk'
        # ftp.connect('139.219.61.61', 21)
        # ftp.login('pass', '1qaz@WSX')
        # bufsize = 1024
        # fp = open('远程账号密码表.xls', 'rb')
        # ftp.storbinary('STOR ' + '远程账号密码表.xls', fp, bufsize)
        # fp.close()
        # ftp.quit()

    def read(self):
        data = xlrd.open_workbook('import_excel.xls')
        table = data.sheets()[0]  # 通过索引顺序获取
        nrows = table.nrows
        return table, nrows


def random_pass():
    """ 生成随机密码函数"""
    tmp = random.sample(string.ascii_letters + string.digits + r'#^&!>./-=+_', 16)
    pwd = ''.join(tmp).strip()
    return pwd


# 修改密码
def ssh(ip, port, username, password, new_password):
    """ 远程连接函数"""
    ssh_ = paramiko.SSHClient()
    ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_.connect(hostname=ip, port=port, username=username, password=password, timeout=30)
        stdin, stdout, stderr = ssh_.exec_command('echo "' + new_password + '" | passwd --stdin root')
        mes = stdout.read().decode('utf-8')
        if 'successfully' in mes or '成功' in mes:
            return 1
        else:
            return 2
    except paramiko.ssh_exception.AuthenticationException:
        return 3
    except:
        return 0
    finally:
        ssh_.close()


with open('./index/id_rsa.pub', 'r') as f:
    id_rsa_pub = f.read()


# 上传公钥
def upload(ip, username, password, port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip, username=username, password=password, port=port)
        stdin, stdout, stderr = ssh.exec_command('cat ~/.ssh/authorized_keys')
        if id_rsa_pub[10:30] not in str(stdout.read()):
            ssh.exec_command('echo ' + id_rsa_pub + ' >> ~/.ssh/authorized_keys')
        else:
            return 1
    except:
        return 0
    finally:
        ssh.close()


# 获取CPU，硬盘内存信息
def handeler(ip, user, password, port):
    ssh_ = paramiko.SSHClient()
    ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_.connect(hostname=ip, port=port, username=user, password=password, timeout=30)
        stdin, stdout, stderr = ssh_.exec_command(
            'cat /proc/cpuinfo\ncat /proc/meminfo | grep MemTotal\nfdisk -l |grep Disk\nprintf bbstart\ncat /etc/redhat-release')
        mes = stdout.read().decode('utf-8')
        ret = re.findall('model name	:(.*)', mes)
        cpu_count = len(ret)
        cpu_name = ret[0]
        system_info = re.findall('bbstart(.*)', mes)
        mem_info = re.findall('MemTotal:(.*)kB', mes)
        hard_info = re.findall(':(.*GB)', mes)
        return cpu_count, cpu_name, system_info[0], str(round(int(mem_info[0]) / 1024 / 1024, 2)) + "GB", ",".join(
            hard_info)
    except:
        return None
    finally:
        ssh_.close()


def progress_bar(a, b):
    bar = '进度 %3.2f%%\r' % (a * 100 / int(b))


def upfile(ip, username, password, port, filename, pdd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    mylog.info("upload/" + filename)
    mylog.info('/' + username + '/' + filename)
    try:
        ssh.connect(hostname=ip, username=username, password=password, port=port, timeout=15)
        ftp = ssh.open_sftp()
        if pdd == 0:
            ftp.put("upload/" + filename, '/' + username + '/' + filename,
                    callback=progress_bar)  # 上传文件,callback=progress_bar
        else:
            ftp.put("upload/" + filename, '/home/' + username + '/' + filename,
                    callback=progress_bar)  # 上传文件
        ftp.close()
        ssh.close()
        return True
    except:
        return False


def downfile(ip, username, password, port, remote_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    mylog.info(os.path.join("download", remote_file.split('/')[-1]))
    mylog.info('/' + username + '/' + remote_file.split('/')[-1])
    try:
        ssh.connect(hostname=ip, username=username, password=password, port=port, timeout=15)
        ftp = ssh.open_sftp()
        ftp.get(remote_file, os.path.join("download", remote_file.split('/')[-1]))  # 下载文件
        ftp.close()
        ssh.close()
        return True
    except:
        return False


def job_bash(ip, username, password, port, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip, username=username, password=password, port=port)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        ssh.close()
        return out + err
    except:
        return "err"
    finally:
        ssh.close()


class linuxCommand:
    def __init__(self):
        self.hostQueue = LinxQueue()
        self.logsQueue = LinxQueue()
        self.logs = []

    def setHostQueue(self, hostname, ip, user, pwd, port, cmd):
        """添加服务器到队列中"""
        self.hostQueue.put({'hostname': hostname, 'ip': ip, 'user': user, 'pwd': pwd, 'port': port, 'cmd': cmd})

    def runQueue(self):
        """取出队列中的所有服务器，执行命令语句"""
        while True:
            host = self.hostQueue.get()
            self.bash(hostname=host['hostname'], ip=host['ip'], username=host['user'], password=host['pwd'],
                      port=host['port'], cmd=host['cmd'])
            self.hostQueue.task_done()

    def bash(self, hostname, ip, username, password, port, cmd):
        """执行命令，将结果存放到日志队列中"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=ip, username=username, password=password, port=port)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            ssh.close()
            self.logsQueue.put((ip, out + err, hostname))
        except socket.timeout:
            self.logsQueue.put((ip, "连接超时", hostname))
        except:
            self.logsQueue.put((ip, "未知错误", hostname))
        finally:
            ssh.close()

    def getlogs(self):
        while True:
            logs = self.logsQueue.get()
            self.logs.append(logs)
            self.logsQueue.task_done()


class smallTools:
    def __init__(self, tools_content):
        self.content = tools_content

    def port(self):
        ip = self.content['ip']
        port = self.content['port']
        try:
            telnetlib.Telnet(ip, int(port), timeout=5)
            return True
        except:
            return False

    def ping(self):
        print(222)
