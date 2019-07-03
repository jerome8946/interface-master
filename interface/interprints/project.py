# -*- coding: utf-8 -*-
import json
import math
from datetime import datetime

from flask import Blueprint, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required

from interface import Auth, common
from interface.extensions import db
from interface.models import Project, Modules, Environment, Parameter, HeaderValue, Transfer

poj_bp = Blueprint('project', __name__, url_prefix='/project', static_folder='static')


@poj_bp.route('/', methods=['GET', 'POST'])
@poj_bp.route('/index', methods=['GET', 'POST'])
@poj_bp.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    """
    项目查询
    :param page: 页数
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        param = []
        page = fromData['page']
        # 拼接查询条件
        if fromData['project_name'] != 'None' and len(fromData['project_name']) > 0:
            param.append(Project.project_name.like("%" + fromData['project_name'] + "%"))
        if fromData['status'] != 'None' and fromData['status'] != '0':
            param.append(Project.status == fromData['status'])
        # 每页显示数
        per_page = current_app.config['INTERFACE_PER_PAGE']
        # 分页对象
        pagination = Project.query.filter(*param).paginate(page, per_page=per_page)

        # 总条数
        count = Project.query.filter(*param).count()
        # # 总页数
        page_count = math.ceil(count / per_page)
        # print('总页数 ', page_count)
        # 当前页数的记录列表
        project = pagination.items
        project_list = []
        for item in project:
            project_dic = {}
            project_dic['project_id'] = item.project_id
            project_dic['project_name'] = item.project_name
            project_dic['project_desc'] = item.project_desc
            project_dic['status'] = item.status
            project_list.append(project_dic)

        list_dic = {}
        list_dic['list'] = project_list
        list_dic['count'] = count
        list_dic['page_count'] = page_count
        list_dic['per_page'] = per_page
        return jsonify(common.trueReturn(list_dic, '项目查询成功'))
    else:
        return jsonify(result)


@poj_bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    项目新增
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        project_name = request.json.get('project_name')
        project_desc = request.json.get('project_desc')
        status = request.json.get('status')
        if status:
            status = '1'
        else:
            status = '2'
        project = Project(project_name=project_name, project_desc=project_desc, status=status)
        db.session.add(project)
        db.session.commit()
        return jsonify(common.trueReturn('', '项目新增成功'))
    else:
        return jsonify(result)


@poj_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    """
    修改项目状态
    :return:
    """
    requests = request.args
    project = Project.query.get_or_404(requests.get('project_id'))
    if requests.get("project_status") == '1':
        project.status = '2'
    else:
        project.status = '1'
    db.session.commit()
    flash('修改成功.', 'success')
    return redirect(url_for('project.index'))


@poj_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    """
    删除项目
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        project_id = request.json.get('project_id')
        Project.query.filter(Project.project_id == project_id).delete(synchronize_session=False)
        db.session.commit()
        db.session.close()
        Modules.query.filter(Modules.project_id == project_id).delete(synchronize_session=False)
        db.session.commit()
        db.session.close()

        environment = Environment.query.with_entities(Environment.env_id).filter(
            Environment.project_id == project_id).all()

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

        Environment.query.filter(Environment.project_id == project_id).delete(synchronize_session=False)
        db.session.commit()
        db.session.close()
        return jsonify(common.trueReturn('', '项目删除成功'))
    else:
        return jsonify(result)


@poj_bp.route('/updateProject', methods=['POST'])
def updateProject():
    """
    项目修改
    :return:
    """

    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        project_id = request.json.get('project_id')
        project_name = request.json.get('project_name')
        project_desc = request.json.get('project_desc')
        status = request.json.get('status')

        project = Project.query.get_or_404(project_id)
        project.project_name = project_name
        if status:
            project.status = 1
        else:
            project.status = 2
        project.project_desc = project_desc
        project.update_time = datetime.now()
        db.session.commit()
        return jsonify(common.trueReturn('', '项目修改成功'))
    else:
        return jsonify(result)


@poj_bp.route('/getProject', methods=['GET', 'POST'])
def getProject():
    """
    查询单个项目
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        project_id = request.json.get('project_id')
        project = Project.query.get_or_404(project_id)
        project_dic = {}
        project_dic['project_id'] = project.project_id
        project_dic['project_name'] = project.project_name
        project_dic['project_desc'] = project.project_desc
        project_dic['status'] = project.status
        return jsonify(common.trueReturn(project_dic, '查询成功'))
    else:
        return jsonify(result)
