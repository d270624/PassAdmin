from django.db import models

"""
数据库说明：
null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
blank 是针对表单的，如果 blank=True，表示你的表单填写该字段时可以不填
"""
TOPIC_CHOICE = (
    ('level1', 'Linux'),
    ('level2', 'Windows'),
    ('level3', '其他'))


class ProjectName(models.Model):  # 添加服务器分组类
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True, verbose_name='ID')  # 自增id
    name = models.CharField(max_length=30, verbose_name='项目名称')

    class Meta:
        verbose_name = "服务器项目组"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class Group(models.Model):  # 添加服务器分组类
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True, verbose_name='ID')  # 自增id
    name = models.CharField(max_length=30, verbose_name='分组名称')

    class Meta:
        verbose_name = "服务器分组"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class PassWord(models.Model):  # 添加服务器类
    def __str__(self):
        return self.hostname

    uid = models.AutoField(primary_key=True)  # 自增id
    hostname = models.CharField(max_length=30, verbose_name='主机名', null=True, blank=True)  # 主机名
    ctime = models.DateTimeField(auto_now=True, null=True)  # 时间
    system = models.CharField(max_length=20, null=True, verbose_name='系统', default='Linux', choices=TOPIC_CHOICE)  # 系统
    ip = models.CharField(verbose_name='IP地址', max_length=30, null=True, blank=True)  # ip
    intranet_ip = models.CharField(verbose_name='内网IP地址', max_length=30, null=True, blank=True)  # 内网ip
    user = models.CharField(max_length=20, verbose_name='高级用户名', null=True, blank=True)  # 账号
    password = models.CharField(max_length=300, verbose_name='密码', null=True, blank=True)  # 密码
    port = models.IntegerField(default=22, verbose_name='端口', null=True, blank=True)  # 端口
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, verbose_name='分组')
    projectName = models.ManyToManyField(ProjectName, blank=True, verbose_name='项目名称')
    system_info = models.CharField(max_length=20, verbose_name='系统版本', null=True, blank=True)  # 系统版本
    cpu_count = models.CharField(max_length=100, verbose_name='cpu核心数', null=True, blank=True)  # cpu信息
    cpu_info = models.CharField(max_length=100, verbose_name='cpu信息', null=True, blank=True)  # cpu信息
    mem_info = models.CharField(max_length=100, verbose_name='内存信息', null=True, blank=True)  # 内存信息
    hard_info = models.CharField(max_length=100, verbose_name='硬盘信息', null=True, blank=True)  # 硬盘信息
    status = models.CharField(max_length=100, verbose_name='状态', null=True, blank=True)  # 状态

    class Meta:
        verbose_name = "服务器信息"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class remarks(models.Model):
    def __str__(self):
        return self.rep

    uid = models.AutoField(primary_key=True)
    rep = models.TextField()  # 备注信息
    host = models.ForeignKey(PassWord, null=True, on_delete=models.CASCADE, verbose_name='对应机器')  # 对应主机信息

    class Meta:
        verbose_name = "备注信息"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class HostTmp(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    unique = models.CharField(max_length=40, unique=True)
    host = models.CharField(max_length=32)
    port = models.IntegerField()
    user = models.CharField(max_length=32)
    auth = models.CharField(max_length=16)
    pkey = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=180, null=True, blank=True)


class Object(models.Model):
    def __str__(self):
        return self.obj_name

    uid = models.AutoField(primary_key=True)
    obj_log = models.CharField(null=True, blank=True, max_length=200)
    obj_name = models.CharField(max_length=50)
    obj_text = models.TextField()

    class Meta:
        verbose_name = "项目模板"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class Project(models.Model):
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='分组')
    name = models.CharField(max_length=50, verbose_name='项目名称')
    host = models.ForeignKey(PassWord, null=True, on_delete=models.CASCADE, verbose_name='服务器')
    template = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='模板')

    class Meta:
        verbose_name = "项目部署"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class Queue(models.Model):
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True)
    user = models.CharField(max_length=50)  # 计划任务创建人
    hostname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)  # 计划名
    time = models.CharField(max_length=50)  # 创建时间
    status = models.CharField(max_length=50, default='')  # 执行状态
    result = models.TextField()  # 执行结果

    class Meta:
        verbose_name = "队列信息"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class linuxTemplate(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)  # linux命令模板名称
    content = models.TextField()  # linux命令


class dataBaseGroup(models.Model):
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名称', null=True, blank=True)

    class Meta:
        verbose_name = "数据库类型"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class dataBase(models.Model):
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True)
    dataGroup = models.ForeignKey(dataBaseGroup, null=True, on_delete=models.CASCADE, verbose_name='数据库类型')
    name = models.CharField(max_length=50, verbose_name='名称', null=True, blank=True)
    ip = models.CharField(max_length=50, verbose_name='ip')
    user = models.CharField(max_length=50, verbose_name='用户名', null=True, blank=True)  # 用户账号
    password = models.CharField(max_length=50, verbose_name='密码', null=True, blank=True)  # 密码
    port = models.CharField(max_length=10, verbose_name="端口", null=True, blank=True)  # 端口
    edition = models.CharField(max_length=50, verbose_name='版本', null=True, blank=True)
    remark = models.CharField(max_length=50, verbose_name='备注', null=True, blank=True)  # 备注
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='分组')

    class Meta:
        verbose_name = "数据库信息"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class UrlMgm(models.Model):
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名称')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='分组')
    url = models.CharField(max_length=200, verbose_name='url地址', null=True, blank=True)
    user = models.CharField(max_length=50, verbose_name='账号', null=True, blank=True)
    password = models.CharField(max_length=50, verbose_name='密码', null=True, blank=True)  # 密码

    class Meta:
        verbose_name = "网址记录"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name


class UrlMgmgroup(models.Model):
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='url分组名称')
    url = models.ManyToManyField(UrlMgm, blank=True, verbose_name='url')

    class Meta:
        verbose_name = "网址记录权限控制"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name


class UsersGroup(models.Model):  # 添加用户分组类
    def __str__(self):
        return self.name

    uid = models.AutoField(primary_key=True, verbose_name='ID')  # 自增id
    name = models.CharField(max_length=30, verbose_name='分组名称', unique=True)
    hostgroup = models.ManyToManyField(Group, verbose_name='机器组', blank=True)  # 设置用户组可以拥有哪些机器组的权限
    host = models.ManyToManyField(PassWord, verbose_name='特定机器', blank=True)
    urlgroup = models.ForeignKey(UrlMgmgroup, verbose_name='Url分组信息', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "用户组"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name


class Users(models.Model):  # 添加用户类
    uid = models.AutoField(primary_key=True)
    user = models.CharField(max_length=30, unique=True)  # 唯一索引
    password = models.CharField(max_length=30)
    user_group = models.ForeignKey(UsersGroup, null=True, on_delete=models.CASCADE, verbose_name='用户分组',
                                   blank=True)  # 一对多
    remark = models.ManyToManyField(remarks, verbose_name='备注信息', blank=True)  # 多对多

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "用户信息"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name  # 效果同上，是复数形式


class supervisor(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey(PassWord, verbose_name='ip', on_delete=models.CASCADE)
    user = models.CharField(max_length=30, default='user', blank=True, verbose_name='账号')
    password = models.CharField(max_length=30, default='123', blank=True, verbose_name='密码')
    port = models.IntegerField(blank=True, default=9001, verbose_name='端口')  # 端口

    def __str__(self):
        return self.ip.ip

    class Meta:
        verbose_name = "supervisor"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name


class ProjectDeploymentRecord(models.Model):
    def __str__(self):
        return self.servername

    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=30, verbose_name='操作人员')
    filename = models.CharField(max_length=30, verbose_name='部署文件名')
    servername = models.CharField(max_length=30, verbose_name='服务器名')
    datetime = models.DateTimeField(auto_now=True)
    projectname = models.CharField(max_length=30, verbose_name='项目名称')

    class Meta:
        verbose_name = "项目部署记录"  # 定义该实体类在 admin 中显示的名字(单数形式)
        verbose_name_plural = verbose_name
