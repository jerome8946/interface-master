# -*- coding: utf-8 -*-
import json
import math
from datetime import datetime

from flask import Blueprint, flash, redirect, url_for, render_template, request, session, current_app, jsonify
from flask_login import login_required

from interface import Auth, common
from interface.extensions import db
from interface.models import Modules, Project, Environment, HeaderValue,Parameter, Transfer

modular_bp = Blueprint('modular', __name__, url_prefix='/modular', static_folder='static')


@modular_bp.route('/', methods=['GET', 'POST'])
@modular_bp.route('/index', methods=['GET', 'POST'])
@modular_bp.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    """
    模块查询
    :param page: 页数
    :return:

    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        param = [Modules.del_status != '0']
        page = fromData['page']
        project_name = fromData['proname']
        modules_name = fromData['modname']
        status = fromData['status']
        # 拼接查询条件
        stmt = Project.query.with_entities(Project.project_id).filter(
            Project.project_name.like("%" + project_name + "%")).subquery()
        if modules_name != 'None' and len(modules_name) > 0:
            param.append(Modules.modules_name.like("%" + modules_name + "%"))
        if status != 'None' and status != '0':
            param.append(Modules.status == status)
        # 每页显示数
        per_page = current_app.config['INTERFACE_PER_PAGE']
        # 分页对象
        pagination = db.session.query(Modules).join(stmt, Modules.project_id == stmt.c.project_id).filter(
            *param).group_by(Modules.modules_id).paginate(
            page,
            per_page=per_page)
        # 总条数
        count = db.session.query(Modules).join(stmt, Modules.project_id == stmt.c.project_id).filter(*param).group_by(
            Modules.modules_id).count()
        # 当前页数的记录列表

        page_count = math.ceil(count / per_page)

        pro_list = Project.query.all()

        modular = pagination.items
        modular_list = []
        for item in modular:
            modular_dic = {}
            modular_dic['mod_id'] = item.modules_id
            modular_dic['pro_name'] = item.project.project_name
            modular_dic['mod_name'] = item.modules_name
            modular_dic['mod_desc'] = item.modules_desc
            modular_dic['status'] = item.status
            modular_list.append(modular_dic)

        list_dic = {}
        list_dic['list'] = modular_list
        list_dic['count'] = count
        list_dic['page_count'] = page_count
        list_dic['per_page'] = per_page

        project = pro_list
        project_list = []
        for item in project:
            project_dic = {}
            project_dic['project_id'] = item.project_id
            project_dic['project_name'] = item.project_name
            project_dic['project_desc'] = item.project_desc
            project_dic['status'] = item.status
            project_list.append(project_dic)

        list_dic['pro_list'] = project_list
        return jsonify(common.trueReturn(list_dic, '模块查询成功'))
    else:
        return jsonify(result)


@modular_bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    模块新增
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        mod_name = request.json.get('mod_name')
        mod_desc = request.json.get('mod_desc')
        status = request.json.get('status')
        pro_id = request.json.get('pro_id')
        if status:
            status = '1'
        else:
            status = '2'
        modules = Modules(modules_name=mod_name, modules_desc=mod_desc, status=status, project_id=pro_id)
        db.session.add(modules)
        db.session.commit()
        return jsonify(common.trueReturn('', '模块新增成功'))
    else:
        return jsonify(result)


@modular_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    """
       修改模块状态
       :return:
       """
    requests = request.args
    project = Modules.query.get_or_404(requests.get('modules_id'))
    if requests.get("modular_status") == '1':
        project.status = '2'
    else:
        project.status = '1'
    db.session.commit()
    flash('修改成功.', 'success')
    return redirect(url_for('modular.index'))


@modular_bp.route('/updateModular', methods=['POST'])
def updateModular():
    """
    模块修改
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        mod_id = request.json.get('mod_id')
        mod_name = request.json.get('mod_name')
        mod_desc = request.json.get('mod_desc')
        pro_id = request.json.get('pro_id')
        status = request.json.get('status')
        modules = Modules.query.get_or_404(mod_id)
        modules.modules_name = mod_name
        modules.modules_desc = mod_desc
        modules.status = status
        modules.project_id = pro_id
        modules.update_time = datetime.now()
        if status:
            modules.status = '1'
        else:
            modules.status = '2'
        db.session.commit()
        return jsonify(common.trueReturn('', '模块修改成功'))
    else:
        return jsonify(result)


@modular_bp.route('/delete', methods=['POST'])
def delete():
    """
    删除模块
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        mod_id = request.json.get('mod_id')
        # Modules.query.filter_by(modules_id=mod_id).update({'del_status': '0'})
        Modules.query.filter(Modules.modules_id == mod_id).delete(synchronize_session=False)
        db.session.commit()
        db.session.close()

        environment = Environment.query.with_entities(Environment.env_id).filter(
            Environment.modules_id == mod_id).all()

        for env in environment:
            parameter = Parameter.query.filter(Parameter.env_id == env.env_id).first()
            if parameter is not None:
                Parameter.query.filter(Parameter.env_id == env.env_id).delete(synchronize_session=False)
                db.session.commit()
                db.session.close()
            # 删除 调用接口
            transfer = Transfer.query.filter(Transfer.tra_need_env_id == env.env_id).first()
            if transfer is not None:
                transfer_all = Transfer.query.filter(Transfer.tra_need_env_id == env.env_id).all()
                for tar in transfer_all:
                    db.session.delete(tar)
                    db.session.commit()
                    db.session.close()
            # 删除信息头
            header = HeaderValue.query.filter(HeaderValue.env_id == env.env_id).first()
            if header is not None:
                HeaderValue.query.filter(HeaderValue.env_id == env.env_id).delete(synchronize_session=False)
                db.session.commit()
                db.session.close()

        Environment.query.filter(Environment.modules_id == mod_id).delete(synchronize_session=False)
        db.session.commit()
        db.session.close()
        return jsonify(common.trueReturn('', '模块删除成功'))
    else:
        return jsonify(result)


@modular_bp.route('/getModular', methods=['GET', 'POST'])
def getProject():
    """
    查询单个模块
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        mod_id = request.json.get('mod_id')
        modules = Modules.query.get_or_404(mod_id)
        modules_dic = {}
        modules_dic['modules_id'] = modules.modules_id
        modules_dic['modules_name'] = modules.modules_name
        modules_dic['modules_desc'] = modules.modules_desc
        modules_dic['project_id'] = modules.project.project_id
        modules_dic['status'] = modules.status
        return jsonify(common.trueReturn(modules_dic, '查询成功'))
    else:
        return jsonify(result)
