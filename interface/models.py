# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from interface import db


class Admin(db.Model, UserMixin):
    """
    用户表
    """
    id = db.Column(db.Integer, primary_key=True)  # 自增id
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码
    name = db.Column(db.String(30))  # 用户名称
    login_time = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get(self, id):
        return self.query.filter_by(id=id).first()


class Project(db.Model):
    """
    项目表
    """
    project_id = db.Column(db.Integer, primary_key=True, comment='项目id')
    # unique = True  分类名称不允许重复
    project_name = db.Column(db.String(30), unique=True, comment='项目名称')
    project_desc = db.Column(db.String(500), comment='项目描述')
    status = db.Column(db.String(10), default='1', comment='项目状态 1启用 ，2禁用')
    update_time = db.Column(db.DateTime, default=datetime.now(), comment='修改时间')
    create_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    # del_status = db.Column(db.String(10), default='1', comment='删除状态 1未删除 0删除')

    module = db.relationship('Modules', back_populates='project',
                             cascade='all , delete-orphan', passive_deletes=True)

    environment = db.relationship('Environment', back_populates='project', cascade='all, delete , delete-orphan')


class Modules(db.Model):
    """
    模块表
    """
    modules_id = db.Column(db.Integer, primary_key=True, comment='模块id')
    # unique = True  分类名称不允许重复
    modules_name = db.Column(db.String(30), unique=True, comment='模块名称')
    modules_desc = db.Column(db.String(500), comment='模块描述')
    status = db.Column(db.String(10), default='1', comment='模块状态 1启用 ，2禁用')
    update_time = db.Column(db.DateTime, default=datetime.now(), comment='修改时间')
    create_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    del_status = db.Column(db.String(10), default='1', comment='删除状态')

    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id', ondelete='CASCADE'), comment='项目表外键')
    project = db.relationship('Project', back_populates='module')

    environment = db.relationship('Environment', back_populates='modules',
                                  cascade='all, delete , delete-orphan')


class Environment(db.Model):
    """
    接口表
    """
    env_id = db.Column(db.Integer, primary_key=True, comment='接口id')
    env_name = db.Column(db.String(30), comment='接口名称')
    env_desc = db.Column(db.String(300), comment='接口名称')
    env_status = db.Column(db.String(10), comment='接口状态 1启用 ，2禁用')
    env_agreement = db.Column(db.String(10), comment='请求协议 get  pos')
    env_transmission = db.Column(db.String(10), comment='传输协议 http  https')
    env_ip = db.Column(db.String(100), comment='接口ip地址')
    env_port = db.Column(db.String(100), comment='接口端口号')
    env_mode = db.Column(db.String(10), comment='接口类型')
    env_path = db.Column(db.String(100), comment='接口路径')
    env_bodyData = db.Column(db.String(500), comment='接口bodyData')
    env_verification = db.Column(db.String(500), comment='校验规则')
    env_update_time = db.Column(db.DateTime, default=datetime.now(), comment='修改时间')
    env_create_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    env_complete = db.Column(db.String(10), default='1', comment='是否开发完成 1完成 ，2未完成')
    env_del_status = db.Column(db.String(10), default='1', comment='删除状态 1未删除  0删除')

    modules_id = db.Column(db.Integer, db.ForeignKey('modules.modules_id'), comment='模块外键')
    modules = db.relationship('Modules', back_populates='environment')

    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), comment='项目外键')
    project = db.relationship('Project', back_populates='environment')

    parameter = db.relationship('Parameter', back_populates='environment',
                                cascade='all, delete , delete-orphan')  # 参数管理表外键

    transfer = db.relationship('Transfer', back_populates='environment', cascade='all, delete-orphan')  # 调用接口

    headerValue = db.relationship('HeaderValue', back_populates='environment',
                                  cascade='all, delete , delete-orphan')  # 参数管理表外键


class HeaderValue(db.Model):
    """
    信息头管理
    """
    header_id = db.Column(db.Integer, primary_key=True, comment='id')
    header_name = db.Column(db.String(30), comment='信息头名称')
    header_value = db.Column(db.String(50), comment='信息头值')

    env_id = db.Column(db.Integer, db.ForeignKey('environment.env_id'), comment='接口表外键')
    environment = db.relationship('Environment', back_populates='headerValue')

    scene_id = db.Column(db.Integer, db.ForeignKey('scene_env.scene_id'), comment='场景表外键')
    sceneEnv = db.relationship('SceneEnv', back_populates='header')


class Parameter(db.Model):
    """
    参数管理表
    """
    par_id = db.Column(db.Integer, primary_key=True, comment='参数id')
    par_variable_name = db.Column(db.String(30), comment='变量名称')
    par_cn_name = db.Column(db.String(30), comment='参数中文名称')
    par_us_name = db.Column(db.String(30), comment='参数英文名称')
    par_type = db.Column(db.String(30), comment='参数类型')
    par_range = db.Column(db.String(30), comment='参数限制范围  0-10-0   0表示最小  10表示最大   0表示小数范围')
    par_date_type = db.Column(db.String(30), comment='日期格式  yyyy-mm-dd')
    par_start_date = db.Column(db.String(30), comment='日期开始时间')
    par_end_date = db.Column(db.String(30), comment='日期结束时间')
    par_required = db.Column(db.String(10), default='1', comment='是否必填 0必填 ，1非必填')
    par_correct = db.Column(db.String(100), comment='正确的参数值')
    par_correct_list = db.Column(db.String(10), default='1', comment='案例值类型 0字符串 ，1 list')
    # par_variable = db.Column(db.String(20), comment='参数变量')

    env_id = db.Column(db.Integer, db.ForeignKey('environment.env_id'), comment='接口表外键')
    environment = db.relationship('Environment', back_populates='parameter')


class Transfer(db.Model):
    """
    接口调用表
    """
    tra_transfer_id = db.Column(db.Integer, primary_key=True, comment='id')
    tra_modulated_env_id = db.Column(db.Integer, comment='被调用的接口id')

    tra_need_env_id = db.Column(db.Integer, db.ForeignKey('environment.env_id'), comment='需要调用的接口id 接口表外键')
    environment = db.relationship('Environment', back_populates='transfer')

    variable = db.relationship('Variable', back_populates='transfer',
                               cascade='all, delete, delete-orphan')


class Variable(db.Model):
    """
    接口返回变量管理
    """
    var_id = db.Column(db.Integer, primary_key=True, comment='id')
    var_regexp = db.Column(db.String(30), comment='正则表达式')
    var_name = db.Column(db.String(30), comment='变量名称')
    var_value = db.Column(db.String(30), comment='变量值')

    # 外键接口调用表
    transfer_id = db.Column(db.Integer, db.ForeignKey('transfer.tra_transfer_id'), comment='接口表外键')
    transfer = db.relationship('Transfer', back_populates='variable')

    scene_id = db.Column(db.Integer, db.ForeignKey('scene_env.scene_id'), comment='场景表外键')
    sceneEnv = db.relationship('SceneEnv', back_populates='variable')


class UserCase(db.Model):
    """
    用例管理
    """
    uc_id = db.Column(db.Integer, primary_key=True, comment='id')
    case_name = db.Column(db.String(30), comment='用例名称')
    case_desc = db.Column(db.String(500), comment='用例描述')
    request_address = db.Column(db.String(30), comment='请求地址')
    email_address = db.Column(db.String(30), comment='邮箱地址')
    case_env = db.relationship('CaseEnv', back_populates='user_case', cascade='all, delete, delete-orphan')
    caseScene = db.relationship('CaseScene', back_populates='user_case', cascade='all, delete, delete-orphan')
    report = db.relationship('Report', back_populates='user_case', cascade='all, delete, delete-orphan')


class CaseEnv(db.Model):
    """
    用例关联的接口
    """
    case_id = db.Column(db.Integer, primary_key=True, comment='id')
    project_id = db.Column(db.Integer, comment='项目id')
    modules_id = db.Column(db.Integer, comment='模块id')
    env_id = db.Column(db.Integer, comment='接口id')
    # 外键接口调用表
    uc_id = db.Column(db.Integer, db.ForeignKey('user_case.uc_id'), comment='接口表外键')
    user_case = db.relationship('UserCase', back_populates='case_env')


class CaseScene(db.Model):
    """
    用例关联的场景
    """
    caseScene_id = db.Column(db.Integer, primary_key=True, comment='id')
    project_id = db.Column(db.Integer, comment='项目id')

    uc_id = db.Column(db.Integer, db.ForeignKey('user_case.uc_id'), comment='用例表外键')
    user_case = db.relationship('UserCase', back_populates='caseScene')

    sceneList_id = db.Column(db.Integer, db.ForeignKey('scene_list.sceneList_id'), comment='场景表外键')
    sceneList = db.relationship('SceneList', back_populates='caseScene')


class TaskManage(db.Model):
    """
    任务管理
    """
    task_id = db.Column(db.Integer, primary_key=True, comment='id')
    task_name = db.Column(db.String(30), comment='id')


class Report(db.Model):
    """
    报告
    """
    report_id = db.Column(db.Integer, primary_key=True, comment='id')
    report_title = db.Column(db.String(50), comment='报告标题')
    report_url = db.Column(db.String(50), comment='请求url')
    report_env_param = db.Column(db.String(100), comment='请求参数')
    report_env_status = db.Column(db.String(10), comment='返回响应码')
    report_env_time = db.Column(db.String(100), comment='响应时间')
    report_env_pass = db.Column(db.Integer, comment='用例执行是否通过  通过0  不通过1')
    report_env_response = db.Column(db.String(100), comment='后台返回数据信息')
    report_create_time = db.Column(db.String(30), comment='创建时间')
    scheduling_id = db.Column(db.String(30), comment='任务ID')
    report_case_type = db.Column(db.String(30), comment='case执行分类')
    # 外键接口调用表
    uc_id = db.Column(db.Integer, db.ForeignKey('user_case.uc_id'), comment='接口表外键')
    user_case = db.relationship('UserCase', back_populates='report')


class Scheduling(db.Model):
    """
    调度任务
    """
    scheduling_id = db.Column(db.String(30), primary_key=True, comment='id')
    scheduling_title = db.Column(db.String(50), comment='任务标题')
    scheduling_cron = db.Column(db.String(50), comment='任务执行时间')
    scheduling_on = db.Column(db.Integer, comment='是否暂停 0执行 1暂停')
    email_address = db.Column(db.String(30), comment='邮箱地址')


class TaskCase(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, comment='id')
    case_id = db.Column(db.Integer, comment='case id')
    scheduling_id = db.Column(db.Integer, comment='任务 id')


class SceneEnv(db.Model):
    """
    场景接口管理表
    """
    scene_id = db.Column(db.Integer, primary_key=True, comment='场景接口id')
    project_id = db.Column(db.Integer, comment='项目id')
    modules_id = db.Column(db.Integer, comment='模块id')
    env_id = db.Column(db.Integer, comment='接口id')
    scene_body = db.Column(db.String(100), comment='场景body')
    number = db.Column(db.Integer, comment='排列顺序')

    header = db.relationship('HeaderValue', back_populates='sceneEnv',
                             cascade='all, delete , delete-orphan')  # 信息头管理表外键

    check = db.relationship('Check', back_populates='sceneEnv',
                            cascade='all, delete , delete-orphan')  # 校验表外键

    variable = db.relationship('Variable', back_populates='sceneEnv',
                               cascade='all, delete, delete-orphan')

    sceneList_id = db.Column(db.Integer, db.ForeignKey('scene_list.sceneList_id'), comment='场景管理表外键')
    sceneList = db.relationship('SceneList', back_populates='sceneEnv')


class SceneList(db.Model):
    """
    场景管理
    """
    sceneList_id = db.Column(db.Integer, primary_key=True, comment='场景id')
    scene_name = db.Column(db.String(100), comment='场景名称')
    project_id = db.Column(db.Integer, comment='项目id')
    scene_desc = db.Column(db.String(100), comment='场景描述')

    sceneEnv = db.relationship('SceneEnv', back_populates='sceneList',
                               cascade='all')

    caseScene = db.relationship('CaseScene', back_populates='sceneList', cascade='all')


class Check(db.Model):
    """
    校验表
    """
    check_id = db.Column(db.Integer, primary_key=True, comment='id')
    check_verification_code = db.Column(db.String(50), comment='校验路径')
    check_agreement_relation = db.Column(db.String(50), comment='校验关系')
    check_verification_value = db.Column(db.String(100), comment='校验值')

    scene_id = db.Column(db.Integer, db.ForeignKey('scene_env.scene_id'), comment='场景表外键')
    sceneEnv = db.relationship('SceneEnv', back_populates='check')
