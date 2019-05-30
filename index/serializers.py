from rest_framework import serializers  # 要用到的包
from .models import *  # 导入表


class Newstagserializer(serializers.ModelSerializer):
    system = serializers.CharField(source='get_system_display')
    group = serializers.CharField()
    project = serializers.SerializerMethodField()

    def get_project(self, obj):
        new = []
        for x in obj.projectName.all():
            new.append(str(x))
        return new

    class Meta:
        model = PassWord
        fields = '__all__'


class templateSer(serializers.ModelSerializer):
    name = serializers.CharField()
    content = serializers.CharField()

    class Meta:
        model = linuxTemplate
        fields = '__all__'


class databaseSer(serializers.ModelSerializer):
    dataGroup = serializers.CharField()  # 用于显示分组名称，不然会显示ID
    group = serializers.CharField()

    class Meta:
        model = dataBase
        fields = '__all__'


class projectSer(serializers.ModelSerializer):
    ip = serializers.SerializerMethodField()
    host_name = serializers.SerializerMethodField()
    template_name = serializers.SerializerMethodField()
    group = serializers.CharField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_ip(self, obj):
        host = obj.host
        ip = host.intranet_ip  # 如果内网IP为空，则使用公网IP
        if ip is None:
            ip = host.ip
        return ip

    def get_host_name(self, obj):
        host = obj.host
        return str(host)

    def get_template_name(self, obj):
        return str(obj.template)


class urlMgmSer(serializers.ModelSerializer):
    group = serializers.CharField()

    class Meta:
        model = UrlMgm
        fields = '__all__'
