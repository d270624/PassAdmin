from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from urllib import parse
from .tools import tools
from .forms import *
from .connect import *
import os, time, json
from index.supervisors import superv
import django.utils.timezone as timezone
import threading
# 定时任务模块
from apscheduler.schedulers.background import BackgroundScheduler
from .serializers import *
from multiprocessing import cpu_count
import logging
# 分页模块
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 日志
mylog = logging.getLogger('django.server')
# 定时任务守护程序
sched = BackgroundScheduler()
sched.start()
# 加密
en = RsaChange()

""""用户相关类"""


# 添加管理员
def add_admin(request):
    sess = request.session.get('user')
    if sess:
        if request.method == 'GET':
            form = AddAdminForm()
            return render(request, 'add_admin.html', locals())
        else:
            form = AddAdminForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                Users(**cd).save()
                return HttpResponse('添加成功')
            else:
                return HttpResponse('信息填写有误')
    else:
        return HttpResponseRedirect('/login/')


# 登录
def login(request):
    if request.method == 'GET':
        # sess = request.session.get('user')
        if 'user' in request.session:
            # 判断是否在session中，如果在就跳转到首页
            return HttpResponseRedirect('/index/')
        else:
            if 'user' in request.COOKIES:
                # 如果不在session中但是是COOKIES中，则将cookies中的信息添加到user中，跳转到首页
                user = request.COOKIES['user']
                request.session['user'] = user
                return HttpResponseRedirect('/index/')
            else:
                # 如果都不在就跳转到登录界面
                form = LoginForm()
                return render(request, 'login.html', locals())
    else:
        form = LoginForm(request.POST)
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        users = Users.objects.filter(user=user)
        if users:
            u = users[0]
            if pwd == u.password:
                request.session['user'] = user
                request.session.set_expiry(0)  # 设置session过期时间为关闭浏览器
                resp = HttpResponseRedirect('/index/')  # 跳到首页
                resp.set_cookie('user', user, 60 * 60 * 24 * 7)  # 设置cookies过期时间为7天
                return resp
            else:
                errMsg = '密码不正确'
                return render(request, 'login.html', locals())
        else:
            errMsg = '账号不存在'
            return render(request, 'login.html', locals())


# 判断用户组
def judgeUserGroup(sess):
    user_group = Users.objects.get(user=sess).user_group  # 取用户组
    if str(user_group) == "AdminGroup":
        return True
    else:
        return False


# 修改用户密码
def modifyUserPassword(request):
    sess = request.session.get('user')
    if sess:
        if request.is_ajax():
            y = request.POST.get("y")
            n = request.POST.get("n")
            c = request.POST.get("c")
            user = request.POST.get("user")
            value = Users.objects.get(user=user)
            if len(n) < 8:
                data = {'status': 'len'}
                return JsonResponse(data)
            elif n != c:
                data = {'status': 'len2'}
                return JsonResponse(data)
            else:
                if str(y) == str(value.password):
                    value.password = n
                    value.save()
                    data = {'status': 'OK'}
                    return JsonResponse(data)
                else:
                    data = {'status': 'error'}
                    return JsonResponse(data)
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


""""首页相关类"""


# 首页
def serverManage(request):
    sess = request.session.get('user')
    if sess:
        value = Object.objects.all()
        if judgeUserGroup(sess):
            auth = 1
            return render(request, 'index.html', locals())
        else:
            auth = 0
            return render(request, 'index.html', locals())
    else:
        return HttpResponseRedirect('/login/')
        # user_group = Users.objects.get(user=sess).user_group  # 取用户组
        # value = Object.objects.all()
        #
        # use = Users.objects.get(user=sess)
        # rep = use.remark.all()  # 获取备注信息
        # all_host = []
        # dd = {}
        # for x in rep:
        #     dd[x.host.uid] = [x.rep, x.uid]  # 将用户的备注信息添加到字典
        # if str(user_group) == "AdminGroup":
        #     auth = 0
        #     pwd = Group.objects.all()  # 获取分组信息
        #     if uid:
        #         uid = int(uid)
        #         # -------------------获取指定分组-----------------------#
        #         groups = Group.objects.get(uid=uid)
        #         host = groups.password_set.all()  # 获取指定分组的全部数据
        #         for x in host:
        #             try:
        #                 reps = dd[x.uid][0]
        #                 rep_uid = dd[x.uid][1]
        #                 a = {'hostname': x.hostname, 'password': en.decrypt(x.password), 'ip': x.ip, 'user': x.user,
        #                      'port': x.port,
        #                      'user_group': x.user_group, 'system': x.get_system_display(), 'uid': x.uid,
        #                      'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': reps, 'rep_uid': rep_uid}
        #                 all_host.append(a)
        #             except:
        #                 a = {'hostname': x.hostname, 'password': en.decrypt(x.password), 'ip': x.ip, 'user': x.user,
        #                      'port': x.port,
        #                      'user_group': x.user_group, 'system': x.get_system_display(), 'uid': x.uid,
        #                      'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': ' ', 'rep_uid': None}
        #                 all_host.append(a)
        #         return render(request, 'index.html', locals())  # 当有uid的时候只显示分组信息
        #     # ------------------获取所有机器------------------------#
        #     data = {}
        #     host = PassWord.objects.all()
        #     return render(request, 'index.html', locals())
        # else:  # --------------------------------------------------------------------以下是普通用户权限
        #     fenlei = UsersGroup.objects.get(name=user_group)
        #     auth = 1
        #     s = [x for x in fenlei.host.all()]  # 获取特殊指定的机器，不管机器是否在在组内都会获取
        #     print(s)
        #     pwd = Group.objects.all()
        #     if uid:
        #         uid = int(uid)
        #         # -------------------获取指定分组-----------------------#
        #         groups = Group.objects.get(uid=uid)
        #         host = groups.password_set.all()  # 获取指定分组的全部数据
        #         for x in s:  # 获取特殊指定的机器，不管机器是否在在组内都会获取
        #             if x.user_group.uid == uid:  # 如果指定组的id等于了特定组的时候才去显示
        #                 try:
        #                     reps = dd[x.uid][0]
        #                     rep_uid = dd[x.uid][1]
        #                     a = {'hostname': x.hostname, 'ip': x.ip, 'user': x.normal_user,
        #                          'port': x.port, 'user_group': x.user_group, 'system': x.get_system_display(),
        #                          'uid': x.uid,
        #                          'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': reps, 'rep_uid': rep_uid}
        #                     all_host.append(a)
        #                 except:
        #                     a = {'hostname': x.hostname, 'ip': x.ip, 'user': x.normal_user,
        #                          'port': x.port, 'user_group': x.user_group, 'system': x.get_system_display(),
        #                          'uid': x.uid,
        #                          'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': ' ', 'rep_uid': None}
        #                     all_host.append(a)
        #         for x in host:  # 在组内的机器显示
        #             if x.uid == uid:
        #                 try:
        #                     reps = dd[x.uid][0]
        #                     rep_uid = dd[x.uid][1]
        #                     a = {'hostname': x.hostname, 'ip': x.ip, 'user': x.normal_user,
        #                          'port': x.port, 'user_group': x.user_group, 'system': x.get_system_display(),
        #                          'uid': x.uid,
        #                          'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': reps, 'rep_uid': rep_uid}
        #                     if a not in all_host:
        #                         all_host.append(a)
        #                 except:
        #                     a = {'hostname': x.hostname, 'ip': x.ip, 'user': x.normal_user,
        #                          'port': x.port, 'user_group': x.user_group, 'system': x.get_system_display(),
        #                          'uid': x.uid,
        #                          'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': ' ', 'rep_uid': None}
        #                     if a not in all_host:
        #                         all_host.append(a)
        #         return render(request, 'index.html', locals())  # 当有uid的时候只显示分组信息
        # ------------------获取所有机器------------------------#
        # for x in s:
        #     try:
        #         reps = dd[x.uid][0]
        #         rep_uid = dd[x.uid][1]
        #         a = {'hostname': x.hostname, 'ip': x.ip, 'user': x.normal_user,
        #              'port': x.port, 'user_group': x.user_group, 'system': x.get_system_display(), 'uid': x.uid,
        #              'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': reps, 'rep_uid': rep_uid}
        #         all_host.append(a)
        #     except:
        #         a = {'hostname': x.hostname, 'ip': x.ip, 'user': x.normal_user,
        #              'port': x.port, 'user_group': x.user_group, 'system': x.get_system_display(), 'uid': x.uid,
        #              'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': ' ', 'rep_uid': None}
        #         all_host.append(a)
        # for x in fenlei.hostgroup.all():  # 获取用户所拥有的所有机器组
        #     groups = Group.objects.get(uid=x.uid)  # 根据分类uid获取组名
        #     host = groups.password_set.all()
        #     for x in host:
        #         try:
        #             reps = dd[x.uid][0]
        #             rep_uid = dd[x.uid][1]
        #             a = {'hostname': x.hostname, 'ip': x.ip, 'user': x.normal_user, 'port': x.port,
        #                  'user_group': x.user_group, 'system': x.get_system_display(), 'uid': x.uid,
        #                  'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': reps, 'rep_uid': rep_uid}
        #             if a not in all_host:
        #                 all_host.append(a)
        #         except:
        #             a = {'hostname': x.hostname, 'ip': x.ip, 'user': x.normal_user, 'port': x.port,
        #                  'user_group': x.user_group, 'system': x.get_system_display(), 'uid': x.uid,
        #                  'cpu_count': x.cpu_count, 'mem_info': x.mem_info, 'rep': ' ', 'rep_uid': None}
        #             if a not in all_host:
        #                 all_host.append(a)
        # return render(request, 'index.html', locals())  # 当没有uid的时候获取所有机器信息
    # else:
    #     return HttpResponseRedirect('/login/')


# 退出页面
def SignOut(request):
    del request.session['user']
    resp = HttpResponseRedirect('/login/')
    resp.delete_cookie('user')
    return resp


# 首页ajax核心处理程序
def getServerList(request):
    sess = request.session.get('user')
    use = Users.objects.get(user=sess)
    rep = use.remark.all()  # 获取备注信息
    status = request.POST.get('status')
    # page_size = int(request.POST.get('pageSize'))
    # page_number = int(request.POST.get('pageNumber'))
    sort = set()
    if judgeUserGroup(sess):
        if request.is_ajax():
            news = PassWord.objects.all()
            serializer = Newstagserializer(news, many=True).data
            if status == 'all':
                for x in serializer:  # 将结果重新组合，把用户备注添加到json中
                    sort.add(x['user_group'])
                    for r in rep:
                        if r.host.uid == x['uid']:
                            x['rep'] = r.rep
                            x['repUid'] = r.uid
                    x['auth'] = 1
                return JsonResponse({'sort': list(sort), 'rows': serializer})
            else:
                de = []
                for index, x in enumerate(serializer, 0):  # 将结果重新组合，把用户备注添加到json中
                    if str(x['user_group']) != status:
                        de.append(index)
                    else:
                        sort.add(x['user_group'])
                        for r in rep:
                            if r.host.uid == x['uid']:
                                x['rep'] = r.rep
                                x['repUid'] = r.uid
                        x['auth'] = 1
                for x in de:
                    serializer[x] = None
                data = list(filter(None, serializer))
                return JsonResponse({'sort': list(sort), 'rows': data})
        else:
            return JsonResponse({"total": 0, "rows": []})
    else:
        if request.is_ajax():
            user_group = Users.objects.get(user=sess).user_group
            fenlei = UsersGroup.objects.get(name=user_group)
            s = {x for x in fenlei.host.all()}  # 1.取单独制定的机器
            for x in fenlei.hostgroup.all():  # 如果不添加组的话会没有结果
                groups = Group.objects.get(uid=x.uid)  # 根据分类uid获取组名
                host = groups.password_set.all()
                y = {x for x in host}  # 2.取组中的所有机器
                s = s | y  # 3.合并机器
            serializer = Newstagserializer(s, many=True).data
            if status == 'all':
                for x in serializer:  # 将结果重新组合，把用户备注添加到json中
                    sort.add(x['user_group'])
                    for r in rep:
                        if r.host.uid == x['uid']:
                            x['rep'] = r.rep
                            x['repUid'] = r.uid
                    x['auth'] = 0
                return JsonResponse({'sort': list(sort), 'rows': serializer})
            else:
                de = []
                for index, x in enumerate(serializer, 0):  # 将结果重新组合，把用户备注添加到json中
                    if str(x['user_group']) != status:
                        de.append(index)
                    else:
                        sort.add(x['user_group'])
                        for r in rep:
                            if r.host.uid == x['uid']:
                                x['rep'] = r.rep
                                x['repUid'] = r.uid
                        x['auth'] = 0
                for x in de:
                    serializer[x] = None
                data = list(filter(None, serializer))
                return JsonResponse({'sort': list(sort), 'rows': data})


# 分页处理
def PageTurning(data, page_size, page_number):
    paginator = Paginator(data, page_size)  # 页面大小
    try:
        contacts = paginator.page(page_number)  # 当前页
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    data = {'total': paginator.count, 'rows': list(contacts)}
    return data


""""服务器相关类"""


# 添加或修改备注
def remark(request):
    sess = request.session.get('user')
    if sess:
        if request.is_ajax():
            uid = request.POST.get('uid')  # 获取服务器uid
            rep_uid = request.POST.get('rep_uid')  # 获取备注uid
            remark_i = request.POST.get('remark_i')  # 获取用户输入内容
            ss = Users.objects.get(user=sess)  # 取用户对象
            if rep_uid == "" or rep_uid == 'undefined':
                sb = remarks.objects.create(rep=remark_i, host=PassWord.objects.get(uid=int(uid)))
                ss.remark.add(sb)
                ss.save()
                data = {'status': '修改成功'}
                return JsonResponse(data)
            else:
                # 修改数据
                ss = ss.remark.get(uid=rep_uid)  # 取用户对象里面的备注对象
                ss.rep = remark_i  # 将用户输入的内容保存到数据库中
                ss.host = PassWord.objects.get(uid=int(uid))  # 取服务器对象并将之保存到服务器中
                ss.save()  # 保存数据
                data = {'status': '修改成功'}
                return JsonResponse(data)
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# 添加服务器
def server_add(request, uid=None):
    sess = request.session.get('user')
    if judgeUserGroup(sess):
        auth = 1
    else:
        auth = 0
    if sess:
        user_group = Users.objects.get(user=sess).user_group  # 取用户组
        if str(user_group) == "AdminGroup":
            if request.method == 'GET':
                form = PassWordForm()
                return render(request, 'form.html', locals())
            else:
                form = PassWordForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    # print(cd['password'])
                    # print(en.encryption(cd['password']))
                    cd['password'] = en.encryption(cd['password'])
                    cd['normal_pwd'] = en.encryption(cd['normal_pwd'])
                    PassWord(**cd).save()
                    mes = '添加成功'
                    return render(request, 'form.html', locals())
                else:
                    mes = '信息填写有误'
                    return render(request, 'form.html', locals())
    return HttpResponseRedirect('/login/')


# 删除机器
def server_del(request, uid):
    sess = request.session.get('user')
    if sess:
        user_group = Users.objects.get(user=sess).user_group  # 取用户组
        if str(user_group) == "AdminGroup":
            obj = PassWord.objects.get(uid=uid)
            obj.delete()
            return HttpResponseRedirect('/index/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# 修改主机数据
def server_modify(request, uid):
    sess = request.session.get('user')
    if judgeUserGroup(sess):
        auth = 1
    else:
        auth = 0
    if sess:
        user_group = Users.objects.get(user=sess).user_group  # 取用户组
        if str(user_group) == "AdminGroup":
            value = PassWord.objects.get(uid=uid)  # 得到指定uid主机的所有信息
            if request.method == 'GET':
                data = {'uid': value.uid, 'hostname': value.hostname, 'system': value.system, 'ip': value.ip,
                        'intranet_ip': value.intranet_ip, 'user': value.user, 'password': en.decrypt(value.password),
                        'normal_user': value.normal_user, 'normal_pwd': en.decrypt(value.normal_pwd),
                        'port': value.port, 'user_group': value.user_group}
                form = PassWordForm(data)  # 将所有数据填入模板中，并显示到界面上
                return render(request, 'update.html', locals())
            else:
                form = PassWordForm(request.POST)  # 将数据放到Form里面
                if form.is_valid():
                    cd = form.cleaned_data
                    cd['password'] = en.encryption(cd['password'])
                    cd['normal_pwd'] = en.encryption(cd['normal_pwd'])
                    PassWord.objects.filter(uid=uid).update(**cd)  # 更新数据
                    mes = '修改成功'
                    return render(request, 'update.html', locals())
                else:
                    mes = '信息填写有误'
                    return render(request, 'form.html', locals())
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# 修改全部密码
def server_pwd_change(request):
    sess = request.session.get('user')
    if sess:
        user_group = Users.objects.get(user=sess).user_group  # 取用户组
        if str(user_group) == "AdminGroup":
            all_host = PassWord.objects.all()
            rett = []
            # for x in all_host:
            #     if x.intranet_ip is None:
            #         ip = x.ip
            #     else:
            #         ip = x.intranet_ip
            #     oldtime = x.ctime.timestamp()
            #     nowtime = time.time()
            #     diff = nowtime - oldtime
            #     if diff >= 60 * 60 * 24 * 7:  # 如果时间差异够的话就可以修改
            #         new_pwd = random_pass()
            #         old_pwd = en.decrypt(x.password)  # 解密
            #         if x.get_system_display() == 'Linux':
            #             ret = ssh(ip=ip, username=x.user, password=old_pwd, port=x.port,
            #                       new_password=new_pwd)
            #             if ret == 1:
            #                 en_pwd = en.encryption(message=new_pwd)  # 加密
            #                 data = {'password': en_pwd, 'ctime': timezone.now()}
            #                 PassWord.objects.filter(uid=x.uid).update(**data)
            #                 rett.append(ip + ' 修改成功')
            #             elif ret == 2:
            #                 rett.append(ip + ' 修改失败')
            #             elif ret == 3:
            #                 rett.append(ip + ' 密码不正确')
            #             elif ret == 0:
            #                 rett.append(ip + ' 无法连接')
            #         elif x.get_system_display() == 'Windows':
            #             f = os.popen(
            #                 'wmic /node:"' + ip + '" /password:"' + old_pwd + '" /user:"' + x.user + '" process call create "cmd.exe /c net user ' + x.user + ' ' + new_pwd + '"')
            #             if 'ReturnValue = 0' in f.read():
            #                 en_pwd = en.encryption(message=new_pwd)  # 加密
            #                 data = {'password': en_pwd, 'ctime': timezone.now()}
            #                 PassWord.objects.filter(uid=x.uid).update(**data)
            #                 rett.append(ip + ' 修改成功')
            #             else:
            #                 rett.append(ip + '修改失败')
            #         else:
            #             rett.append(ip + ' 暂不支持')
            #     else:  # 不能修改
            #         rett.append(ip + '修改失败,距离上次修改未到一星期')
            ex = Excel()
            ex.update(all_host)
            ex.save()
            return HttpResponse(rett)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# 导入Excel
def server_import(request):
    sess = request.session.get('user')
    if sess:
        if request.method == 'POST':
            myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                return HttpResponse("没有选择上传文件")
            e_file = open('import_excel.xls', 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                e_file.write(chunk)
            e_file.close()
            e = Excel()
            ret = []
            try:
                table, nrows = e.read()
                for x in range(nrows):
                    if x == 0:
                        continue
                    cd = {
                        'user_group': Group.objects.get(name=table.row_values(x)[0]),  # 得到组对象后添加到数据库中
                        'hostname': table.row_values(x)[1],
                        'system': table.row_values(x)[2],
                        'ip': table.row_values(x)[3],
                        'intranet_ip': table.row_values(x)[4],
                        'user': table.row_values(x)[5],
                        'password': table.row_values(x)[6],
                        'normal_user': table.row_values(x)[7],
                        'normal_pwd': table.row_values(x)[8],
                        'port': int(table.row_values(x)[9])
                    }
                    if cd['intranet_ip'] == "":
                        ip = cd['ip']
                    else:
                        ip = cd['intranet_ip']
                    try:
                        PassWord.objects.get(ip=ip)  # 查询是否存在
                        ret.append({ip: '已存在'})
                    except PassWord.MultipleObjectsReturned:  # 查到重复，不处理
                        ret.append({ip: '已存在'})
                    except PassWord.DoesNotExist:  # 不存在
                        if cd['system'].lower() == "linux":
                            cd['system'] = 'level1'
                        elif cd['system'].lower() == "windows":
                            cd['system'] = 'level2'
                        else:
                            cd['system'] = 'level3'
                        cd['password'] = en.encryption(cd['password'])
                        cd['normal_pwd'] = en.encryption(cd['normal_pwd'])
                        PassWord(**cd).save()
                        ret.append({ip: '添加成功'})
                return HttpResponse(ret)
            except:
                return HttpResponse('请检查Excel内容是否正确！')
    else:
        return HttpResponseRedirect('/login/')


"""服务器信息获取类"""


# 获取机器信息处理程序
def getSystemInfoHandler(request):
    sess = request.session.get('user')
    if sess:
        user_group = Users.objects.get(user=sess).user_group  # 取用户组
        if str(user_group) == "AdminGroup":
            host = PassWord.objects.all()
            for x in host:
                ip = x.ip
                user = x.user
                password = en.decrypt(x.password)
                port = x.port
                system = x.system
                uid = x.uid
                if str(system) == "level1":
                    ret = handeler(ip, user, password, port)
                    if ret:
                        cpu_count, cpu_name, system_info, mem_info, hard_info = ret
                        cd = {'system_info': system_info, 'cpu_count': cpu_count, 'cpu_info': cpu_name,
                              'mem_info': mem_info,
                              'hard_info': hard_info, 'status': "开机"}
                        PassWord.objects.filter(uid=uid).update(**cd)  # 更新数据
                    else:
                        pass
                else:
                    pass
            return HttpResponse('更新成功')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


"""服务器批量脚本执行类"""


# 树形
def serverList(request):
    sess = request.session.get('user')
    if judgeUserGroup(sess):
        auth = 1
    else:
        auth = 0
    if sess:
        user_group = Users.objects.get(user=sess).user_group  # 取用户组
        if str(user_group) == "AdminGroup":
            return render(request, 'shell.html', locals())
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# 树形
def serverListHandler(request):
    host = PassWord.objects.all()
    data = []
    fl = {}
    group = Group.objects.all()
    for index, x in enumerate(group, 1):
        b = {'id': index - 100, 'pId': 0, 'name': x.name, 'open': 'false'}  # 分组
        fl[x.name] = index - 100
        data.append(b)
    for x in host:
        if x.user_group:
            data.append({'id': x.uid, 'name': x.hostname, 'ip': x.ip, 'pId': fl[str(x.user_group)]})
        else:
            data.append({'id': x.uid, 'name': x.hostname, 'ip': x.ip, 'pId': 0})
    return JsonResponse(json.dumps(data), safe=False)


# 批量执行脚本
def serverBatchRun(request):
    """后期改实时方法：结果存放在数据库中，然后再写一个函数判读队列是否为空，前端负责展示运行状态：运行中，完成两种状态
    运行完以后用ajax将所有的运行结果打印出来，或者换成实时读取的方法
    """
    sess = request.session.get('user')
    if sess:
        if judgeUserGroup(sess):
            run_linux = linuxCommand()
            if request.is_ajax():
                cmd = request.POST.get('cmd')
                uid_list = json.loads(request.POST.get("uid"))
                for x in uid_list:
                    value = PassWord.objects.get(uid=x)
                    user = value.user
                    ip = value.ip
                    hostname = value.hostname
                    pwd = en.decrypt(value.password)
                    port = value.port
                    run_linux.setHostQueue(hostname, ip, user, pwd, port, cmd)  # 将节点添加到队列中

                thread_list = []
                for i in range(cpu_count() * 2):
                    threadrun = threading.Thread(target=run_linux.runQueue)
                    thread_list.append(threadrun)
                for i in range(cpu_count() * 2):
                    threadlogs = threading.Thread(target=run_linux.getlogs)
                    thread_list.append(threadlogs)
                for th in thread_list:
                    th.setDaemon(True)
                    th.start()
                run_linux.hostQueue.join()  # 阻塞等待结束
                run_linux.logsQueue.join()  # 阻塞等待结束
                mylog.info('队列结束')
                logs = run_linux.logs
                data = []
                for ip, result, hostname in logs:
                    data.append({'ip': ip, 'result': result.replace('\n', '<br>'), 'hostname': hostname})
                return JsonResponse({'data': data})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# 显示linux模板
def showServerTemplate(request):
    sess = request.session.get('user')
    if sess:
        res = linuxTemplate.objects.all()
        serializer = templateSer(res, many=True).data
        return JsonResponse({'rows': serializer})
    else:
        return HttpResponseRedirect('/login/')


# 添加和修改linux模板
def addServerTemplate(request):
    sess = request.session.get('user')
    if sess:
        if request.is_ajax():
            temp_uid = request.POST.get('temp_uid')
            temp_name = request.POST.get('temp_name')
            temp_text = request.POST.get('temp_text')
            if temp_uid:
                tmp = linuxTemplate.objects.get(uid=int(temp_uid))
                tmp.name = temp_name
                tmp.content = temp_text
                tmp.save()
                mes = '修改成功'
            else:
                dic = {
                    'name': temp_name,
                    'content': temp_text,
                }
                obj = linuxTemplate(**dic)
                obj.save()
                mes = '添加成功'
            return JsonResponse({'mes': mes})
    else:
        return HttpResponseRedirect('/login/')


# 删除linux模板
def delServerTemplate(request):
    sess = request.session.get('user')
    if sess:
        uid = request.POST.get('uid')
        try:
            res = linuxTemplate.objects.get(uid=uid)
            res.delete()
            mes = '删除成功'
        except:
            mes = '删除失败'
        return JsonResponse({'mes': mes})
    else:
        return HttpResponseRedirect('/login/')


# 远程连接处理程序
def webssh(request, uid):
    sess = request.session.get('user')
    if sess:
        if request.method == 'GET':
            return render(request, 'webssh.html', locals())
        if request.method == 'POST':
            success = {'code': 0, 'message': None, 'error': None}
            try:
                # post_data = request.POST.get('data')
                # data = json.loads(post_data)
                # auth = data.get('auth')
                # if auth == 'key':
                #     pkey = request.FILES.get('pkey')
                #     key_content = pkey.read().decode('utf-8')
                #     data['pkey'] = key_content
                # else:
                data = PassWord.objects.get(uid=int(uid))
                if data.intranet_ip is None:
                    ip = data.ip
                else:
                    ip = data.intranet_ip
                if judgeUserGroup(sess):
                    data = {'host': ip,
                            'port': data.port,
                            'user': data.user,
                            'auth': 'pwd',
                            'password': en.decrypt(data.password)}
                else:
                    data = {'host': ip,
                            'port': data.port,
                            'user': data.normal_user,
                            'auth': 'pwd',
                            'password': en.decrypt(data.normal_pwd)}
                password = data.get('password')
                password = base64.b64encode(password.encode('utf-8'))  # 编码
                data['password'] = password.decode('utf-8')
                unique = tools.unique()
                data['unique'] = unique
                valid_data = tools.ValidationData(data)  # 将字段存进数据库
                if valid_data.is_valid():
                    valid_data.save()
                    success['message'] = unique
                else:
                    error_json = valid_data.errors.as_json()
                    success['code'] = 1
                    success['error'] = error_json
                return JsonResponse(success)
            except:
                success['code'] = 1
                success['error'] = '发生未知错误'
                return JsonResponse(success)

    else:
        return HttpResponseRedirect('/login/')


"""服务器文件处理类"""


# 上传文件
def ufile(request):
    sess = request.session.get('user')
    if sess:
        if request.method == 'POST':
            uid = request.POST.get('uid')
            path = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
            if not path:
                return HttpResponse("没有选择上传文件")
            e_file = open(os.path.join("upload", path.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in path.chunks():  # 分块写入文件
                e_file.write(chunk)
            e_file.close()
            obj = PassWord.objects.get(uid=uid)
            if obj.intranet_ip is None:
                ip = obj.ip
            else:
                ip = obj.intranet_ip
            if judgeUserGroup(sess):
                user = obj.user
                pwd = en.decrypt(obj.password)
                pdd = 1
            else:
                user = obj.normal_user
                pwd = en.decrypt(obj.normal_pwd)
                pdd = 0
            if upfile(ip, user, pwd, obj.port, path.name, pdd):
                os.remove(os.path.join("upload", path.name))
                data = {'status': 1}  # ajax上传成功
                return JsonResponse(data)
            data = {'status': 0}  # 上传失败
            return JsonResponse(data)
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# 下载文件
def down_handler(request):
    sess = request.session.get('user')
    if sess:
        with open('xshell.reg', 'rb') as model_excel:
            result = model_excel.read()
        response = HttpResponse(result)
        response['Content-Disposition'] = 'attachment; filename=xshell.reg'
        return response
        # if request.method == 'POST':
        #     path = request.POST.get('path')
        #     uid = request.POST.get('uid')
        #     obj = PassWord.objects.get(uid=uid)
        #     if judgeUserGroup(sess):  # 判断用户是管理员还是普通用户
        #         # user = obj.user
        #         # pwd = en.decrypt(obj.password)
        #     else:
        #         user = obj.normal_user
        #         pwd = en.decrypt(obj.normal_pwd)
        #     ret = downfile(ip=obj.ip, username=user, password=pwd, port=obj.port, remote_file=path)
        #     print(ret)
        # else:
        #     return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


"""调用本地程序类"""


# 执行xshell
def getXshell(request, uid):
    sess = request.session.get('user')
    if sess:
        if judgeUserGroup(sess):
            value = PassWord.objects.get(uid=int(uid))  # 得到指定uid主机的所有信息
            if value.ip is None:
                ip = value.intranet_ip
            else:
                ip = value.ip
            if value.normal_pwd == None or value.normal_user == None:
                return HttpResponse("<html><script>alert('该服务器普通账号或密码没有设置，请联系管理员')</script></html>")
            else:
                response = HttpResponse("", status=302)
                response['Location'] = "ssh://" + value.user + ":" + parse.quote(en.decrypt(
                    value.password)) + "@" + ip + ":" + str(value.port)
                return response
        else:
            value = PassWord.objects.get(uid=int(uid))  # 得到指定uid主机的所有信息
            if value.ip is None:
                ip = value.intranet_ip
            else:
                ip = value.ip
            if value.normal_pwd == None or value.normal_user == None:
                return HttpResponse("<html><script>alert('该服务器普通账号或密码没有设置，请联系管理员')</script></html>")
            else:
                response = HttpResponse("", status=302)
                response['Location'] = "ssh://" + value.normal_user + ":" + parse.quote(en.decrypt(
                    value.password)) + "@" + ip + ":" + str(value.port)
                return response
    else:
        return HttpResponseRedirect('/login/')


# 执行xftp
def getXftp(request, uid):
    sess = request.session.get('user')
    if sess:
        if judgeUserGroup(sess):
            value = PassWord.objects.get(uid=int(uid))  # 得到指定uid主机的所有信息
            if value.ip is None:
                ip = value.intranet_ip
            else:
                ip = value.ip
            if value.normal_pwd == None or value.normal_user == None:
                return HttpResponse("<html><script>alert('该服务器普通账号或密码没有设置，请联系管理员')</script></html>")
            else:
                response = HttpResponse("", status=302)
                response['Location'] = "sftp://" + value.user + ":" + parse.quote(en.decrypt(
                    value.password)) + "@" + ip + ":" + str(value.port)
                return response
        else:
            value = PassWord.objects.get(uid=int(uid))  # 得到指定uid主机的所有信息
            if value.ip is None:
                ip = value.intranet_ip
            else:
                ip = value.ip
            if value.normal_pwd == None or value.normal_user == None:
                return HttpResponse("<html><script>alert('该服务器普通账号或密码没有设置，请联系管理员')</script></html>")
            else:
                response = HttpResponse("", status=302)
                response['Location'] = "sftp://" + value.normal_user + ":" + parse.quote(en.decrypt(
                    value.password)) + "@" + ip + ":" + str(value.port)
                return response
    else:
        return HttpResponseRedirect('/login/')


"""项目部署类"""


# 项目部署
def project(request):
    sess = request.session.get('user')
    if sess:
        if request.method == 'GET':
            if judgeUserGroup(sess):
                auth = 1
            else:
                auth = 0
            value = Object.objects.all()
            return render(request, 'project.html', locals())
        else:
            pro = Project.objects.all()
            serializer = projectSer(pro, many=True).data
            return JsonResponse({'rows': serializer})
    else:
        return HttpResponseRedirect('/login/')


# 添加项目
def edit_project(request):
    sess = request.session.get('user')
    if sess:
        value = Object.objects.all()
        if request.method == 'GET':
            if judgeUserGroup(sess):
                auth = 1
            else:
                auth = 0
            form = ObjectForm()
            return render(request, 'edit_project.html', locals())
        else:
            form = ObjectForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                Object(**cd).save()
                mes = '添加成功'
                return HttpResponseRedirect('/edit_project/')
            else:
                mes = '信息填写有误'
                return render(request, 'edit_project.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# 修改项目
def obj_modify(request):
    sess = request.session.get('user')
    if sess:
        if request.is_ajax():
            uid = request.POST.get("uid")
            obj = Object.objects.get(uid=uid)
            data = {'obj_name': obj.obj_name, 'obj_text': obj.obj_text, 'uid': obj.uid, 'obj_log': obj.obj_log}
            return JsonResponse(data)
    else:
        return HttpResponseRedirect('/login/')


# 修改项目处理程序
def obj_modify_handler(request):
    sess = request.session.get('user')
    if sess:
        if request.is_ajax():
            uid = request.POST.get("uid")
            form = ObjectForm(request.POST)  # 将数据放到Form里面
            if form.is_valid():
                cd = form.cleaned_data
                Object.objects.filter(uid=uid).update(**cd)
                data = {'status': '修改成功'}
                return JsonResponse(data)

    else:
        return HttpResponseRedirect('/login/')


# 删除项目
def obj_del(request, uid):
    sess = request.session.get('user')
    if sess:
        obj = Object.objects.get(uid=uid)
        obj.delete()
        return HttpResponseRedirect('/edit_project/')
    else:
        return HttpResponseRedirect('/login/')


# 项目部署核心处理程序
def obj_hander(request):
    sess = request.session.get('user')
    data = {}
    if sess:
        if request.method == 'POST':
            uid = request.POST.get('uid')
            obj = PassWord.objects.get(uid=int(uid))
            obj_uid = request.POST.get('obj_uid')
            time_status = request.POST.get('time_status')
            obj_time = request.POST.get('obj_time')
            qname = request.POST.get('qname')
            if time_status == "1":  # 如果等于1就执行定时任务
                if obj_time == '':
                    data['result'] = "time_error"
                    return JsonResponse(data)
                else:
                    times = obj_time.replace('T', ' ')
                    if times.count(':') == 1:
                        times = times + ":00"
                    sched.add_job(job_timing, 'date', run_date=times,
                                  args=(uid, obj_uid, qname))  # 将定时任务添加到计划任务列表
                    dic = {
                        'hostname': obj.hostname,
                        'user': sess,
                        'name': qname,
                        'time': times,
                        'status': '未到执行时间',  # 未执行
                    }
                    obj = Queue(**dic)
                    obj.save()
                    data['result'] = "que_true"
                    return JsonResponse(data)
            else:
                return JsonResponse(job_normal(uid, data, obj_uid))
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


# 定时任务程序
def job_timing(uid, obj_uid, qname):
    obj = PassWord.objects.get(uid=int(uid))
    if obj.intranet_ip is None:
        ip = obj.ip
    else:
        ip = obj.intranet_ip

    que = Queue.objects.get(name=qname)
    pro = Object.objects.get(uid=obj_uid)
    res = job_bash(ip=ip, username=obj.user, password=en.decrypt(obj.password), port=obj.port, cmd=pro.obj_text)
    if res == "err":
        que.status = '执行失败'
        que.result = "脚本执行失败，请检查服务器配置或者脚本模板内容"
    else:
        res = res.replace('\n', '\\n')
        que.status = '执行完成'
        que.result = "文件上传到服务器成功！\\n" + res
    que.save()


# 非定时任务程序
def job_normal(uid, data, obj_uid):
    obj = PassWord.objects.get(uid=int(uid))
    if obj.intranet_ip is None:
        ip = obj.ip
    else:
        ip = obj.intranet_ip
    pro = Object.objects.get(uid=obj_uid)
    s = job_bash(ip=ip, username=obj.user, password=en.decrypt(obj.password), port=obj.port, cmd=pro.obj_text)
    # 执行完批量语句以后，开始执行日志查看系统

    if s == "err":
        data['result'] = "server_error"
        return data
    else:
        data['result'] = "文件上传成功！开始执行项目部署脚本\n\n" + s + "\n脚本部署完成\n开始显示日志详情:\n"
        return data


# 队列展示界面
def task_queue(request):
    sess = request.session.get('user')
    if judgeUserGroup(sess):
        auth = 1
    else:
        auth = 0
    if sess:
        res = Queue.objects.filter(user=sess)
        return render(request, 'queue.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# 删除队列
def task_queue_del(request, uid):
    sess = request.session.get('user')
    if sess:
        res = Queue.objects.get(uid=uid)
        res.delete()
        return HttpResponseRedirect('/queue/')
    else:
        return HttpResponseRedirect('/login/')


# 小工具
def small_tool(request):
    sess = request.session.get('user')
    if sess:
        if judgeUserGroup(sess):
            auth = 1
        else:
            auth = 0
        return render(request, 'tools.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# 小工具处理程序
def get_tools(request):
    sess = request.session.get('user')
    if sess:
        post_body = request.body
        json_result = json.loads(post_body.decode('utf-8'))
        tools_type = json_result.get('type')
        tools_content = json_result.get('content')
        t_tools = smallTools(tools_content)
        if tools_type == 'port':
            if t_tools.port():
                data = {'status': '开通'}
            else:
                data = {'status': '关闭'}
        if tools_type == 'ping':
            t_tools.ping()
        return JsonResponse(data)
    else:
        return HttpResponseRedirect('/login/')


"""数据库处理程序"""


# 数据展示
def showDatabase(request):
    sess = request.session.get('user')
    if judgeUserGroup(sess):
        auth = 1
    else:
        auth = 0
    if sess:
        if request.method == 'GET':
            form = dataBaseForm()
            return render(request, 'database.html', locals())
        else:
            status = request.POST.get('status')
            if status == 'all':
                data = dataBase.objects.all()
            else:
                name = dataBaseGroup.objects.get(name=status)
                data = name.database_set.all()  # 获取指定组内的所有内容
            serializer = databaseSer(data, many=True).data
            dataGroup = dataBaseGroup.objects.all().values('name')
            sort = []
            for x in dataGroup:
                sort.append(x['name'])
            return JsonResponse({'rows': serializer, 'sort': sort})
    else:
        return HttpResponseRedirect('/login/')


# 添加数据库和修改

def addDatabase(request):
    sess = request.session.get('user')
    if sess:
        form = dataBaseForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            dataBase(**cd).save()
            messages.success(request, "添加成功")
        else:
            messages.success(request, "添加失败")
        return HttpResponseRedirect('/showDatabase/')
    else:
        return HttpResponseRedirect('/login/')


# 修改数据库
def updateDatabase(request):
    sess = request.session.get('user')
    if sess:
        if request.is_ajax():
            uid = request.POST.get("uid")
            obj = dataBase.objects.get(uid=uid)
            data = {'uid': obj.uid, 'name': obj.name, 'dataGroup': str(obj.dataGroup), 'ip': obj.ip, 'user': obj.user,
                    'password': obj.password,
                    'port': obj.port, 'edition': obj.edition, 'remark': obj.remark}
            return JsonResponse(data)
        elif request.method == 'POST':
            form = dataBaseForm(request.POST)
            uid = request.POST.get('uid')
            if form.is_valid():
                cd = form.cleaned_data
                dataBase.objects.filter(uid=uid).update(**cd)
                messages.success(request, "修改成功")
                return HttpResponseRedirect('/showDatabase/')
            else:
                messages.success(request, "修改失败")
                return HttpResponseRedirect('/showDatabase/')
    else:
        return HttpResponseRedirect('/login/')


# 删除数据库
def delDatabase(request, uid):
    sess = request.session.get('user')
    if sess:
        obj = dataBase.objects.get(uid=uid)
        obj.delete()
        messages.success(request, "删除成功")
        return HttpResponseRedirect('/showDatabase/')
    else:
        return HttpResponseRedirect('/login/')


# Url管理程序
def showUrlMgm(request):
    sess = request.session.get('user')
    if sess:
        if judgeUserGroup(sess):
            auth = 1
        else:
            auth = 0
        if request.method == 'GET':
            form = UrlMgm()
            return render(request, 'urlmgm.html', locals())
        else:
            if auth == 1:
                data = UrlMgm.objects.all()
                serializer = urlMgmSer(data, many=True).data
            else:
                auth = Users.objects.get(user=sess)  # 用户用户名查找到用户对象
                user_group = auth.user_group  # 通过用户对象查找到用户组
                urlgroup = user_group.urlgroup  # 通过用户组得到url组
                url = urlgroup.url  # 通过url组得到url组对象
                data = url.all()  # 通过url组对象获取所有组内信息
                # data = auth.user_group.urlmgm.url.all() # 省略写法
                serializer = urlMgmSer(data, many=True).data
            return JsonResponse({'rows': serializer})
    else:
        return HttpResponseRedirect('/login/')


# supervisors
def showSupervisor(request):
    sess = request.session.get('user')
    if sess:
        if judgeUserGroup(sess):
            auth = 1
        else:
            auth = 0
        s = supervisor.objects.all()
        status = request.POST.get('status')
        data = []
        if request.method == 'GET':
            return render(request, 'supervisor.html', locals())
        elif status == 'list':  # 获取所有服务器列表
            for x in s:
                if x.ip.intranet_ip is None:
                    ip = x.ip.ip
                else:
                    ip = x.ip.intranet_ip
                res = {'text': ip, 'id': x.id}
                data.append(res)
            data = json.dumps(data)
            return HttpResponse(data)
        elif status == 'all':
            for x in s:  # 这边只读取一台即可
                if x.ip.intranet_ip is None:
                    ip = x.ip.ip
                else:
                    ip = x.ip.intranet_ip
                sup = superv(ip=ip, user=x.user, password=x.password, port=x.port)
                data = sup.getAllProcessInfo()  # 获取服务器所有信息
                for i in data:
                    i['id'] = x.id
                data = json.dumps(data)
                return HttpResponse(data)
        elif status == 'first':
            id = request.POST.get('id')
            res = supervisor.objects.get(id=int(id))
            if res.ip.intranet_ip is None:
                ip = res.ip.ip
            else:
                ip = res.ip.intranet_ip
            sup = superv(ip=ip, user=res.user, password=res.password, port=res.port)
            data = sup.getAllProcessInfo()
            for i in data:
                i['id'] = res.id
            data = json.dumps(data)
            return HttpResponse(data)
        else:
            return HttpResponse({'status': 'error'})
    else:
        return HttpResponseRedirect('/login/')


# supervisor处理函数
def super_handler(request):
    action = request.GET.get('action', '')
    processname = request.GET.get('processname', '')
    id = request.GET.get('id', '')
    res = supervisor.objects.get(id=id)
    if res.ip.intranet_ip is None:
        ip = res.ip.ip
    else:
        ip = res.ip.intranet_ip
    sup = superv(ip=ip, user=res.user, password=res.password, port=res.port)
    if action == 'restart':
        sup.restart(processname)
        messages.success(request, "重启成功")
        return HttpResponseRedirect('/showSupervisor/')
    if action == 'start':
        res = sup.start(processname)
        if res:
            messages.success(request, "启动成功")
        else:
            messages.success(request, "启动失败")
        return HttpResponseRedirect('/showSupervisor/')
    if action == 'stop':
        res = sup.stop(processname)
        if res:
            messages.success(request, "停止成功")
        else:
            messages.success(request, "停止失败")
        return HttpResponseRedirect('/showSupervisor/')
    if action == 'startAllProcesses':
        res = sup.start_all()
        if res:
            messages.success(request, "启动成功")
        else:
            messages.success(request, "启动失败")
        return HttpResponseRedirect('/showSupervisor/')
    if action == 'stopAllProcesses':
        res = sup.stop_all()
        if res:
            messages.success(request, "停止成功")
        else:
            messages.success(request, "停止失败")
        return HttpResponseRedirect('/showSupervisor/')
    if action == 'restartService':
        res = sup.restart_all()
        if res:
            messages.success(request, "重启成功")
        else:
            messages.success(request, "重启失败")
        return HttpResponseRedirect('/showSupervisor/')
    if action == 'reloadConfig':
        res = sup.restart_all()
        if res:
            messages.success(request, "重启加载配置成功")
        else:
            messages.success(request, "重启加载配置失败")
        return HttpResponseRedirect('/showSupervisor/')


def getSuperConf(request):
    sess = request.session.get('user')
    if sess:
        if judgeUserGroup(sess):
            id = request.POST.get('id')
            content = request.POST.get('content')
            res = supervisor.objects.get(id=id)
            if res.ip.intranet_ip is None:
                ip = res.ip.ip
            else:
                ip = res.ip.intranet_ip
            res = job_bash(ip=ip, username=res.ip.user, password=en.decrypt(res.ip.password), port=res.ip.port,
                           cmd="cat /etc/supervisord.conf")
            return JsonResponse({'data': res})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def saveSuperConf(request):
    sess = request.session.get('user')
    if sess:
        if judgeUserGroup(sess):
            id = request.POST.get('id')
            content = request.POST.get('content')
            content = content.replace('\r', '')
            with open('upload/supervisord.conf', 'w', encoding='utf-8') as f:
                f.writelines(content)
            res = supervisor.objects.get(id=id)
            if res.ip.intranet_ip is None:
                ip = res.ip.ip
            else:
                ip = res.ip.intranet_ip
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname=ip, username=res.ip.user, password=en.decrypt(res.ip.password), port=res.ip.port,
                            timeout=15)
                ftp = ssh.open_sftp()
                ftp.put('upload/supervisord.conf', '/etc/supervisord.conf')
                ftp.close()
                return JsonResponse({'data': 'sucess'})
            except:
                return JsonResponse({'data': 'err'})
            finally:
                ssh.close()
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')
