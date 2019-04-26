from django.contrib import admin
from .models import *

admin.site.register(PassWord)
admin.site.register(Group)
admin.site.register(Users)
admin.site.register(UsersGroup)
admin.site.register(Queue)
admin.site.register(remarks)
admin.site.register(dataBase)
admin.site.register(dataBaseGroup)
admin.site.register(Project)
admin.site.register(UrlMgm)


# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'password', 'isActive')
