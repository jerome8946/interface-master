# -*- coding: utf-8 -*-
import json
import math

from flask import Blueprint, render_template, flash, redirect, url_for, session, current_app, make_response, jsonify
from flask_login import login_required

from interface import db, Auth, common
from interface.forms import EnvironmentSelectForm
from interface.models import Project, Modules, Environment, Transfer, Variable, Parameter, HeaderValue

from flask import request

env_bp = Blueprint('env', __name__, url_prefix='/env', static_folder='static', template_folder='templates')


@env_bp.route('/', methods=['GET', 'POST'])
@env_bp.route('/index', methods=['GET', 'POST'])
@env_bp.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    """
    接口查询
    :param page: 页数
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        param = [Environment.env_del_status != '0']

        page = fromData['page']
        project_name = fromData['proname']
        modules_name = fromData['modname']
        env_name = fromData['envname']
        status = fromData['status']
        # 拼接查询条件
        project = Project.query.with_entities(Project.project_id).filter(
            Project.project_name.like("%" + project_name + "%")).subquery()

        modules = Modules.query.with_entities(Modules.modules_id).filter(
            Modules.modules_name.like("%" + modules_name + "%")).subquery()

        if env_name != 'None' and len(env_name) > 0:
            param.append(Environment.env_name.like("%" + env_name + "%"))
        if status != 'None' and status != '0':
            param.append(Environment.env_status == status)
        # 每页显示数
        per_page = current_app.config['INTERFACE_PER_PAGE']
        # 分页对象
        pagination = Environment.query.join(project,
                                            Environment.project_id == project.c.project_id).join(
            modules, Environment.modules_id == modules.c.modules_id).filter(*param).group_by(
            Environment.env_id).paginate(
            page,
            per_page=per_page)
        # 总条数
        count = Environment.query.join(project,
                                       Environment.project_id == project.c.project_id).join(
            modules, Environment.modules_id == modules.c.modules_id).filter(*param).group_by(Environment.env_id).count()
        page_count = math.ceil(count / per_page)
        environment = pagination.items

        env_list = []
        for item in environment:
            env_dic = {}
            env_dic['env_id'] = item.env_id
            env_dic['env_name'] = item.env_name
            env_dic['env_desc'] = item.env_desc
            env_dic['env_status'] = item.env_status
            env_dic['env_agreement'] = item.env_agreement
            env_dic['env_transmission'] = item.env_transmission
            env_dic['env_ip'] = item.env_ip
            env_dic['env_port'] = item.env_port
            env_dic['env_mode'] = item.env_mode
            env_dic['env_path'] = item.env_path
            env_dic['env_bodyData'] = item.env_bodyData
            env_dic['env_verification'] = item.env_verification
            env_dic['env_complete'] = item.env_complete
            env_dic['modules_id'] = item.modules.modules_id
            env_dic['project_id'] = item.project.project_id
            env_dic['project_name'] = item.project.project_name
            env_dic['modules_name'] = item.modules.modules_name
            env_list.append(env_dic)

        pro_list = Project.query.all()
        project = pro_list
        project_list = []
        for item in project:
            project_dic = {}
            project_dic['project_id'] = item.project_id
            project_dic['project_name'] = item.project_name
            project_dic['project_desc'] = item.project_desc
            project_dic['status'] = item.status
            project_list.append(project_dic)

        list_dic = {}
        list_dic['count'] = count
        list_dic['page_count'] = page_count
        list_dic['per_page'] = per_page
        list_dic['list'] = env_list
        list_dic['pro_list'] = project_list

        return jsonify(common.trueReturn(list_dic, '接口查询成功'))
    else:
        return jsonify(result)


@env_bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    模块接口
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        list_transfer = []
        for transfer in request.json.get("tra_table"):
            list_variables = []
            for variables in transfer['varTable']:
                variable = Variable(var_regexp=variables['var_regexp'], var_name=variables['var_name'])
                list_variables.append(variable)
            transfer_db = Transfer(tra_modulated_env_id=transfer['tar_env_id'], variable=list_variables)
            list_transfer.append(transfer_db)

        list_parm = []
        for parm in request.json.get('parm_table'):
            parameter = Parameter(
                par_variable_name=parm['env_parameter_par_variable_name'],
                par_cn_name=parm['env_parameter_par_cn_name'],
                par_us_name=parm['env_parameter_par_en_name'],
                par_type=parm['env_parameter_par_type'],
                par_range=parm['env_parameter_par_range'],
                par_date_type=str(parm['par_date_type']), par_start_date=parm['par_start_date'],
                par_end_date=parm['par_end_date'], par_required=parm['env_parameter_par_required'],
                par_correct=parm['env_parameter_par_correct_value'],
                par_correct_list=parm['par_correct_list'],
            )
            list_parm.append(parameter)

        headerList = []
        if len(request.json.get('headerValue')):
            for hear in request.json.get('headerValue'):
                hearders = HeaderValue(header_name=hear['header_name'], header_value=hear['header_value'])
                headerList.append(hearders)

        env = Environment(env_name=request.json.get('env_name'), env_desc=request.json.get('env_desc'),
                          env_status=request.json.get('env_status'),
                          env_agreement=request.json.get('env_agreement'),
                          env_transmission=request.json.get('env_transmission'),
                          env_ip=request.json.get('env_ip'), env_port=request.json.get('env_port'),
                          env_path=request.json.get('env_path'), env_bodyData=request.json.get('env_bodyData'),
                          env_verification=request.json.get('env_verification'),
                          env_complete=request.json.get('env_complete'), project_id=request.json.get('project_id'),
                          modules_id=request.json.get('modules_id'), parameter=list_parm, transfer=list_transfer,
                          headerValue=headerList)
        db.session.add(env)
        db.session.commit()

        return jsonify(common.trueReturn('', '接口新增成功'))
    else:
        return jsonify(result)


@env_bp.route('/selectModular', methods=['GET', 'POST'])
def select_modular():
    """
    根据项目查询模块
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        project_id = fromData['project_id']
        model = Modules.query.with_entities(Modules.modules_id, Modules.modules_name).filter(
            Modules.project_id == project_id).all()
        model_dict = []
        for p, k in model:
            model_json = {}
            model_json['modules_id'] = p
            model_json['modules_name'] = k
            model_dict.append(model_json)
        return jsonify(common.trueReturn(model_dict, '模块查询成功'))
    else:
        return jsonify(result)


@env_bp.route('/selectProject', methods=['GET', 'POST'])
def select_project():
    """
    根据项目查询模块
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        project = Project.query.with_entities(Project.project_id, Project.project_name).all()
        project_dict = []
        for p, k in project:
            pro_json = {}
            pro_json['project_id'] = p
            pro_json['project_name'] = k
            project_dict.append(pro_json)
        return jsonify(common.trueReturn(project_dict, '项目查询成功'))
    else:
        return jsonify(result)


@env_bp.route('/selectEnv', methods=['GET', 'POST'])
def select_env():
    """
    根据模块查询接口
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        modules_id = fromData['modules_id']
        env = Environment.query.with_entities(Environment.env_id, Environment.env_name).filter(
            Environment.modules_id == modules_id).all()
        env_dict = []
        for p, k in env:
            env_json = {}
            env_json['env_id'] = p
            env_json['env_name'] = k
            env_dict.append(env_json)
        return jsonify(common.trueReturn(env_dict, '接口查询成功'))
    else:
        return jsonify(result)


@login_required
def select_env_only(modules_id, env_name):
    """
    查询接口名称是否存在
    :param modules_id:  模块ID
    :param env_name:    接口名称
    :return:
    """
    env = Environment.query.with_entities(Environment.env_id).filter(
        Environment.modules_id == modules_id, Environment.env_name == env_name).first()
    return env


@env_bp.route('/update', methods=['GET', 'POST'])
def update():
    """
       模块修改
       :return:
       """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        # 删除参数
        parameter = Parameter.query.filter(Parameter.env_id == fromData["env_id"]).first()
        if parameter is not None:
            Parameter.query.filter(Parameter.env_id == fromData["env_id"]).delete(synchronize_session=False)
            db.session.commit()
        # 删除 调用接口
        transfer = Transfer.query.filter(Transfer.tra_need_env_id == fromData["env_id"]).first()
        if transfer is not None:
            transfer_all = Transfer.query.filter(Transfer.tra_need_env_id == fromData["env_id"]).all()
            for tar in transfer_all:
                db.session.delete(tar)
                db.session.commit()
            # Transfer.query.filter(Transfer.tra_need_env_id == fromData["env_id"]).delete(synchronize_session=False)
            # db.session.commit()

        # 删除信息头
        header = HeaderValue.query.filter(HeaderValue.env_id == fromData["env_id"]).first()
        if header is not None:
            HeaderValue.query.filter(HeaderValue.env_id == fromData["env_id"]).delete(synchronize_session=False)
            db.session.commit()

        # 接口调用模块
        for transfer in fromData['tra_table']:
            list_variables = []
            for variables in transfer['varTable']:
                variable = Variable(var_regexp=variables['var_regexp'], var_name=variables['var_name'])
                list_variables.append(variable)
            transfer_db = Transfer(tra_modulated_env_id=transfer['tar_env_id'],
                                   tra_need_env_id=fromData["env_id"], variable=list_variables)
            db.session.add(transfer_db)
            db.session.commit()
            # list_transfer.append(transfer_db)

        # 信息头新增
        if len(fromData['headerValue']):
            for hear in fromData['headerValue']:
                hearders = HeaderValue(header_name=hear['header_name'], header_value=hear['header_value'],
                                       env_id=fromData["env_id"])
                db.session.add(hearders)
                db.session.commit()

        # 接口参数模块
        if len(fromData['parm_table']):
            for parm in fromData['parm_table']:
                parameter = Parameter(
                    par_variable_name=parm['env_parameter_par_variable_name'],
                    par_cn_name=parm['env_parameter_par_cn_name'],
                    par_us_name=parm['env_parameter_par_en_name'],
                    par_type=parm['env_parameter_par_type'],
                    par_range=parm['env_parameter_par_range'],
                    par_date_type=str(parm['par_date_type']), par_start_date=parm['par_start_date'],
                    par_end_date=parm['par_end_date'],
                    par_required=parm['env_parameter_par_required'],
                    par_correct=parm['env_parameter_par_correct_value'],
                    par_correct_list=parm['par_correct_list'],
                    env_id=fromData["env_id"])
                db.session.add(parameter)
                db.session.commit()

        # 修改接口主表
        environment = Environment.query.get_or_404(fromData["env_id"])
        environment.env_name = fromData['env_name']
        environment.env_desc = fromData['env_desc']
        environment.env_status = fromData['env_status']
        environment.env_agreement = fromData['env_agreement']
        environment.env_transmission = fromData['env_transmission']
        environment.env_ip = fromData['env_ip']
        environment.env_port = fromData['env_port']
        environment.env_path = fromData['env_path']
        environment.env_bodyData = fromData['env_bodyData']
        environment.env_verification = fromData['env_verification']
        # environment.env_complete = fromData['env_complete']
        environment.project_id = fromData['project_id']
        environment.modules_id = fromData['modules_id']
        db.session.commit()
        return jsonify(common.trueReturn('', '接口编辑成功'))
    else:
        return jsonify(result)


@env_bp.route('/updateEnv', methods=['GET', 'POST'])
def updateEnv():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        env_id = request.json.get('env_id')
        env = Environment.query.get_or_404(env_id)
        envJson = {}
        envJson['project_id'] = env.project_id
        envJson['modules_id'] = env.modules_id
        envJson['env_name'] = env.env_name
        envJson['env_desc'] = env.env_desc
        envJson['env_transmission'] = env.env_transmission
        envJson['env_agreement'] = env.env_agreement
        envJson['env_ip'] = env.env_ip
        envJson['env_path'] = env.env_path
        envJson['env_port'] = env.env_port
        envJson['env_bodyData'] = env.env_bodyData
        envJson['env_verification'] = env.env_verification
        envJson['env_status'] = env.env_status
        envJson['env_complete'] = env.env_complete
        envJson['env_id'] = env.env_id

        transfer_jsonarray = []
        for transfer in env.transfer:
            transfer_dict = {}
            transfer_dict['tra_transfer_id'] = transfer.tra_transfer_id
            transfer_dict['tra_need_env_id'] = transfer.tra_need_env_id
            transfer_dict['tar_env_id'] = transfer.tra_modulated_env_id
            tra_modulated_env = Environment.query.get_or_404(transfer.tra_modulated_env_id)
            transfer_dict['tar_pro_id'] = tra_modulated_env.project_id
            transfer_dict['tar_mod_id'] = tra_modulated_env.modules_id
            transfer_dict['tar_pro_name'] = tra_modulated_env.project.project_name
            transfer_dict['tar_mod_name'] = tra_modulated_env.modules.modules_name
            transfer_dict['tar_env_name'] = tra_modulated_env.env_name
            variable_list = []
            for variable in transfer.variable:
                variable_dict = {}
                variable_dict['var_id'] = variable.var_id
                variable_dict['transfer_id'] = variable.transfer_id
                variable_dict['var_name'] = variable.var_name
                variable_dict['var_regexp'] = variable.var_regexp
                variable_dict['var_value'] = variable.var_value
                variable_list.append(variable_dict)
            transfer_dict['varTable'] = variable_list
            transfer_jsonarray.append(transfer_dict)

        parameter_list = []
        for parameter in env.parameter:
            parameter_dict = {}
            parameter_dict['env_parameter_par_variable_name'] = parameter.par_variable_name
            parameter_dict['env_parameter_par_cn_name'] = parameter.par_cn_name
            parameter_dict['env_parameter_par_correct_value'] = parameter.par_correct
            parameter_dict['par_date_type'] = parameter.par_date_type
            parameter_dict['par_end_date'] = parameter.par_end_date
            parameter_dict['par_id'] = parameter.par_id
            parameter_dict['env_parameter_par_range'] = parameter.par_range
            parameter_dict['env_parameter_par_required'] = parameter.par_required
            parameter_dict['par_start_date'] = parameter.par_start_date
            parameter_dict['env_parameter_par_type'] = parameter.par_type
            parameter_dict['env_parameter_par_en_name'] = parameter.par_us_name
            parameter_dict['par_correct_list'] = parameter.par_correct_list
            parameter_dict['env_id'] = parameter.env_id
            # parameter_dict['env_parameter_par_variable'] = parameter.par_variable
            parameter_list.append(parameter_dict)

        headerValue_list = []
        for header in env.headerValue:
            headerValue_dict = {}
            headerValue_dict['header_name'] = header.header_name
            headerValue_dict['header_value'] = header.header_value
            headerValue_dict['env_id'] = header.env_id
            headerValue_list.append(headerValue_dict)

        envJson['tra_table'] = json.dumps(transfer_jsonarray, ensure_ascii=False)
        envJson['parm_table'] = json.dumps(parameter_list, ensure_ascii=False)
        envJson['headerValue'] = json.dumps(headerValue_list, ensure_ascii=False)

        return jsonify(common.trueReturn(envJson, '查询成功'))
    else:
        return jsonify(result)


@env_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        env_id = request.json.get('env_id')
        Environment.query.get_or_404(env_id)
        Environment.query.filter_by(env_id=env_id).delete()
        db.session.commit()
        return jsonify(common.trueReturn('', '接口删除成功'))
    else:
        return jsonify(result)


@env_bp.route('/update_status', methods=['GET', 'POST'])
def update_status():
    """
   修改模块状态
   :return:
    """
    requests = request.args
    env = Environment.query.get_or_404(requests.get('env_id'))
    if requests.get("env_status") == '1':
        env.env_status = '2'
    else:
        env.env_status = '1'
    db.session.commit()
    flash('修改成功.', 'success')
    return redirect(url_for('env.index'))
