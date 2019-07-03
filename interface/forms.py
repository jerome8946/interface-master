# -*- coding: utf-8 -*-
"""
表单
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField, \
    FieldList, FormField, DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL, Regexp

from interface.models import Project


class LoginForm(FlaskForm):
    """
    登录
    """
    username = StringField('账号', validators=[DataRequired(message=u"用户名不能为空")
        , Length(1, 20, message=u'长度位于1~20之间')], render_kw={'placeholder': u'输入用户名'})
    password = PasswordField('密码', validators=[DataRequired(message=u"密码不能为空")
        , Length(5, 20, message=u'长度位于5~20之间')], render_kw={'placeholder': u'输入密码'})
    remember = BooleanField('Remember me', validators=[DataRequired()])
    submit = SubmitField('登录')


class ProjectAddForm(FlaskForm):
    """
    项目新增
    """
    project_name = StringField(u'项目名称', validators=[DataRequired(message=u"项目不能为空")
        , Length(1, 30, message=u'长度位于1~30之间')], render_kw={'placeholder': u'输入项目名称'})
    project_desc = TextAreaField('项目描述', validators=[DataRequired(message=u"项目描述不能为空")
        , Length(1, 500, message=u'长度位于1~500之间')],
                                 render_kw={'placeholder': u'输入项目描述', "style": "height:150px;width:300px"})
    status = BooleanField('是否禁用', default=False)
    submit = SubmitField('提交')


class ProjectSelectForm(FlaskForm):
    """
    项目查询
    """
    project_name = StringField(u'项目名称', render_kw={'placeholder': u'输入项目名称'})
    status = SelectField(u'项目状态', choices=[('0', '全部'), ('1', '启用'), ('2', '禁用')])
    create_time = StringField('创建时间', render_kw={'placeholder': u'输入项目名称'})
    submit = SubmitField('查询')


class ModulesAddForm(FlaskForm):
    """
    模块新增
    """
    project = SelectField(u'项目名称', validators=[DataRequired()], coerce=int)
    modules_name = StringField(u'模块名称', validators=[DataRequired(message=u"模块不能为空")
        , Length(1, 30, message=u'长度位于1~30之间')], render_kw={'placeholder': u'输入模块名称'})
    modules_desc = TextAreaField(u'模块描述', validators=[DataRequired(message=u'模块描述不能为空')
        , Length(1, 500, message=u'长度位于1~500之间')],
                                 render_kw={'placeholder': u'输入模块描述', "style": "height:150px;width:300px"})
    status = BooleanField(u'是否禁用', default=False)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(ModulesAddForm, self).__init__(*args, **kwargs)
        self.project.choices = [(v.project_id, v.project_name) for v in
                                Project.query.with_entities(Project.project_id, Project.project_name).all()]


#
class ModulesSelectForm(FlaskForm):
    """模块查询"""
    project_name = StringField(u'项目名称', render_kw={'placeholder': u'输入项目名称'})
    modules_name = StringField(u'模块名称', render_kw={'placeholder': u'输入模块名称'})
    status = SelectField(u'模块状态', choices=[('0', '全部'), ('1', '启用'), ('2', '禁用')])
    create_time = StringField(u'创建时间')
    submit = SubmitField(u'查询')


class Variables(FlaskForm):
    """
    参数模块
    """
    var_regexp = StringField(u'正则表达式', validators=[Regexp], render_kw={'placeholder': u'输入正则表达式'})
    var_variable_name = StringField(u'变量名称', render_kw={'placeholder': u'输入变量名称'})


class Transfer(FlaskForm):
    """
      接口调用模块
    """
    tra_project_name = SelectField(u'项目名称', validators=[DataRequired()], choices=[('0', '请选择')], coerce=int)
    tra_modules_name = SelectField(u'模块名称', validators=[DataRequired()], choices=[('0', '请选择')], coerce=int)
    tra_env_name = SelectField(u'接口名称名称', validators=[DataRequired()], choices=[('0', '请选择')], coerce=int)
    tra_variables = FieldList(FormField(Variables), min_entries=1)


class Parameter(FlaskForm):
    """
    参数模块
    """
    par_cn_name = StringField(u'中文名称', validators=[DataRequired()], render_kw={'placeholder': u'输入中文名称'})
    par_en_name = StringField(u'英文名称', validators=[DataRequired()], render_kw={'placeholder': u'输入英文名称'})
    par_type = SelectField(u'参数类型', choices=[('0', 'String'), ('1', 'Number'), ('2', 'Date')])
    par_required = SelectField(u'参数类型', choices=[('0', '必填'), ('1', '非必填')])
    par_range = StringField(u'参数限制范围', validators=[DataRequired()], render_kw={'placeholder': u'输入参数限制范围'})
    par_date_type = DateTimeField(u'日期格式', render_kw={'placeholder': u'日期格式'})
    par_start_date = DateTimeField(u'开始时间', render_kw={'placeholder': u'开始时间'})
    par_end_date = StringField(u'结束时间', render_kw={'placeholder': u'结束时间'})
    par_correct_value = StringField(u'案例参数', render_kw={'placeholder': u'输入案例参数值'})
    par_correct_start_date = DateTimeField(u'案例开始时间', render_kw={'placeholder': u'输入案例开始时间'})
    par_correct_end_date = StringField(u'案例结束时间', render_kw={'placeholder': u'输入案例结束时间'})


class EnvironmentAddForm(FlaskForm):
    """
    接口新增
    """
    env_name = StringField(u'名称', validators=[Length(1, 30, message=u'长度位于1~30之间')],
                           render_kw={'placeholder': u'输入接口名称'})
    env_desc = TextAreaField(u'描述', validators=[Length(1, 100, message=u'长度位于1~100之间')],
                             render_kw={'placeholder': u'输入接口描述'})
    env_status = SelectField(u'状态', choices=[('0', '全部'), ('1', '启用'), ('2', '禁用')])
    env_agreement = SelectField(u'请求协议', choices=[('0', 'GET'), ('1', 'POST')])
    env_transmission = SelectField(u'传输协议', choices=[('0', 'HTTP'), ('1', 'HTTPS')])
    env_ip = StringField(u'ip地址', render_kw={'placeholder': u'输入接口ip地址'})
    env_port = StringField(u'端口号', render_kw={'placeholder': u'输入接口端口号'})
    env_mode = StringField(u'类型', render_kw={'placeholder': u'输入接口类型'})
    env_path = StringField(u'路径', render_kw={'placeholder': u'输入接口路径'})
    env_headers = StringField(u'headers', render_kw={'placeholder': u'输入接口headers'})
    env_verification = StringField(u'校验规则', render_kw={'placeholder': u'输入校验规则'})
    env_complete = BooleanField(u'是否开发完成', default=True)
    env_transfer = FieldList(FormField(Transfer))
    env_parameter = FieldList(FormField(Parameter), min_entries=1)
    submit = SubmitField(u'提交')


class EnvironmentSelectForm(FlaskForm):
    """
    接口查询
    """
    project_name = StringField(u'项目名称', render_kw={'placeholder': u'输入项目名称'})
    modules_name = StringField(u'模块名称', render_kw={'placeholder': u'输入模块名称'})
    env_name = StringField(u'接口名称', render_kw={'placeholder': u'输入接口名称'})
    env_path = StringField(u'请求路径', render_kw={'placeholder': u'输入接口请求路径'})
    env_status = SelectField(u'是否禁用', choices=[('0', '全部'), ('1', '启用'), ('2', '禁用')])
    env_complete = SelectField(u'是否开发完成', choices=[('0', '全部'), ('1', '完成'), ('2', '未完成')])
    create_time = StringField('创建时间', render_kw={'placeholder': u'创建时间'})

    submit = SubmitField('查询')


class CaseSelectForm(FlaskForm):
    """
    用例查询
    """
    case_name = StringField(u'用例名称', render_kw={'placeholder': u'输入用例名称'})
    submit = SubmitField('查询')