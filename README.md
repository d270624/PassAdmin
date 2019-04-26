# PassAdmin安装教程
### 系统：centos 7 ：

### 1.安装python环境

#### 安装EPEL和IUS软件源

```python
yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
```

####  安装Python3.6
`yum install python36u -y`

####  创建python3连接符
`ln -s /bin/python3.6 /bin/python3`

####  安装pip3
`yum install python36u-pip -y`

####  创建pip3链接符
`ln -s /bin/pip3.6 /bin/pip3`

---
###  2.安装依赖包
`yum install python36u-devel.x86_64`

---
###  3.安装所有模块

`pip3.6 install -r requirement.txt`

---
###  4.git下载代码到本地
`git clone git@github.com:d270624/PassAdmin.git`

---
###  5.执行构建数据库结构代码
```
cd PassAdmin
python3.6 manage.py makemigrations
python3.6 manage.py migrate
```

---
### 运行程序
`python3.6 manage runserver 0.0.0.0:8000`
