# PassAdmin安装教程
### 系统：centos 7 ：

### 1.安装python环境
http://www.6fantian.com/web/#/2?page_id=148

###  2.安装依赖包
yum install python36u-devel.x86_64

###  3.安装所有模块

pip3.6 install -r requirement.txt

###  4.git下载代码到本地
git clone git@github.com:d270624/PassAdmin.git

###  5.执行代码
cd PassAdmin
python3.6 manage runserver 0.0.0.0:8000
