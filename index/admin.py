from django.contrib import admin
from .models import *


# Register your models here.
class UsersGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'urlgroup')
    filter_horizontal = ('hostgroup', 'host')


class UrlMgmgroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('url',)


class PassWordAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'system', 'ip', 'intranet_ip', 'user', 'group')
    fieldsets = (
        ('main', {
            'fields': ('hostname', 'system', 'ip', 'intranet_ip', 'user', 'password', 'port', 'group', 'projectName')}),
        ('optional',
         {'fields': ('system_info', 'cpu_count', 'cpu_info', 'mem_info', 'hard_info', 'status')}),
    )
    filter_horizontal = ('projectName',)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'password', 'user_group', 'fullName')


class supervisorAdmin(admin.ModelAdmin):
    list_display = ('ip', 'user', 'password', 'port')


admin.site.register(PassWord, PassWordAdmin)
admin.site.register(Group)
admin.site.register(ProjectName)
admin.site.register(Users, UsersAdmin)
admin.site.register(UsersGroup, UsersGroupAdmin)
admin.site.register(Queue)
admin.site.register(remarks)
admin.site.register(dataBase)
admin.site.register(dataBaseGroup)
admin.site.register(Project)
admin.site.register(UrlMgm)
admin.site.register(ProjectDeploymentRecord)
admin.site.register(UrlMgmgroup, UrlMgmgroupAdmin)
admin.site.register(supervisor, supervisorAdmin)
