from django import forms
from .models import *


class PassWordForm(forms.ModelForm):  # 自动生成表单
    def __init__(self, *args, **kwargs):
        super(PassWordForm, self).__init__(*args, **kwargs)
        self.fields['hostname'].required = False  # 是否必填
        self.fields['ip'].required = False
        self.fields['user'].required = False
        self.fields['password'].required = False
        self.fields['port'].required = False
        self.fields['group'].required = False
        self.fields['system_info'].required = False
        self.fields['cpu_count'].required = False
        self.fields['cpu_info'].required = False
        self.fields['mem_info'].required = False
        self.fields['hard_info'].required = False
        self.fields['status'].required = False

    class Meta:
        # 1.定义关联的Models
        model = PassWord
        # 2.定义要生成控件的字段
        fields = '__all__'  # ['uname','upwd'],生成所有或者列表中的数据
        # 3.为生成控件的字段指定标签
        labels = {
            'hostname': '主机名',
            'system': '系统',
            'ip': 'IP地址',
            'intranet_ip': '内网IP',
            'user': '用户名',
            'password': '密码',
            'port': '端口',
            'group': '分组',
        }
        widgets = {
            'hostname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'system': forms.Select(attrs={'class': 'form-control'}),
            'ip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'intranet_ip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'port': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }


class AddAdminForm(forms.ModelForm):  # 自动生成表单
    class Meta:
        # 1.定义关联的Models
        model = Users
        # 2.定义要生成控件的字段
        fields = '__all__'  # ['uname','upwd'],生成所有或者列表中的数据
        # 3.为生成控件的字段指定标签
        labels = {
            'user': '用户名',
            'password': '密码',
            'email': '邮箱'
        }
        widgets = {
            'user': forms.TextInput(attrs={
                'class': 'text',
                "onfocus": "this.value = '';",
                "onblur": "if (this.value == '') {this.value = '账号';}",
                'value': '账号',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'text',
                "onfocus": "this.value = '';",
            })
        }


class LoginForm(forms.ModelForm):  # 自动生成表单
    class Meta:
        # 1.定义关联的Models
        model = Users
        # 2.定义要生成控件的字段
        fields = ['user', 'password']  # 生成所有或者列表中的数据
        # 3.为生成控件的字段指定标签
        labels = {
            'user': '用户名',
            'password': '密码',
        }
        widgets = {
            'user': forms.TextInput(attrs={
                'class': 'text',
                "onfocus": "this.value = '';",
                "onblur": "if (this.value == '') {this.value = '账号';}",
                'value': '账号',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'text',
                "onfocus": "this.value = '';",
            })
        }


class ObjectForm(forms.ModelForm):  # 自动生成表单
    def __init__(self, *args, **kwargs):
        super(ObjectForm, self).__init__(*args, **kwargs)
        self.fields['obj_log'].required = False  # 是否必填

    class Meta:
        # 1.定义关联的Models
        model = Object
        # 2.定义要生成控件的字段
        fields = ['obj_name', 'obj_text', 'obj_log']  # 生成所有或者列表中的数据
        # 3.为生成控件的字段指定标签
        labels = {
            'obj_name': '项目名称',
            'obj_text': '执行语句',
            'obj_log': '日志路径',
        }
        widgets = {
            'obj_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'obj_log': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'obj_text': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }


class dataBaseForm(forms.ModelForm):  # 自动生成表单
    def __init__(self, *args, **kwargs):
        super(dataBaseForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False  # 是否必填
        self.fields['user'].required = False  # 是否必填
        self.fields['password'].required = False  # 是否必填
        self.fields['port'].required = False  # 是否必填
        self.fields['edition'].required = False  # 是否必填
        self.fields['remark'].required = False  # 是否必填

    class Meta:
        # 1.定义关联的Models
        model = dataBase
        # 2.定义要生成控件的字段
        fields = '__all__'  # 生成所有或者列表中的数据
        # 3.为生成控件的字段指定标签
        labels = {
            'dataGroup': '数据库类型',
            'name': '名称',
            'ip': 'IP地址',
            'user': '用户名',
            'password': '密码',
            'port': '端口',
            'edition': '版本',
            'remark': '备注',
        }
        widgets = {
            'dataGroup': forms.Select(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',

            }),
            'port': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'edition': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'ip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
            'remark': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '选填',
            }),
        }
