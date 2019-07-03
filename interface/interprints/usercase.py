# -*- coding: utf-8 -*-
import datetime
import json
import math
import os
import time
import uuid

from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify, session, current_app
from flask_login import login_required

from interface import db, Auth, common
from interface.EmailOperate import send_mail_with_file

from interface.forms import CaseSelectForm
from interface.interprints.reportLog import getExecl
from interface.mock.implement import test_case
from interface.models import UserCase, CaseEnv, Environment, Modules, Project, Report, CaseScene, SceneList

case_bp = Blueprint('case', __name__, url_prefix='/case', static_folder='static', template_folder='templates')
current_path = os.path.abspath('.')


@case_bp.route('/', methods=['GET', 'POST'])
@case_bp.route('/index', methods=['GET', 'POST'])
def index():
    """
    用例查询
    :param page: 页数
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        page = fromData['page']
        case_name = fromData['case_name']
        param = []

        # form = CaseSelectForm()
        # case_name = ""
        # param = []
        # if request.method == 'POST':
        #     case_name = form.case_name.data
        param.append(UserCase.case_name.like("%" + case_name + "%"))
        # 每页显示数
        per_page = current_app.config['INTERFACE_PER_PAGE']
        # 分页对象
        pagination = UserCase.query.filter(*param).paginate(page, per_page=per_page)
        # 总条数
        count = UserCase.query.filter(*param).count()
        page_count = math.ceil(count / per_page)
        caseList = pagination.items
        case_list = []
        for item in caseList:
            case_dic = {}
            case_dic['case_id'] = item.uc_id
            case_dic['case_name'] = item.case_name
            case_dic['case_desc'] = item.case_desc
            case_dic['request_address'] = item.request_address
            case_dic['email_address'] = item.email_address
            case_list.append(case_dic)

        list_dic = {}
        list_dic['list'] = case_list
        list_dic['count'] = count
        list_dic['page_count'] = page_count
        list_dic['per_page'] = per_page
        return jsonify(common.trueReturn(list_dic, '接口查询成功'))
    else:
        return jsonify(result)


@case_bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    用例新增
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        if fromData is not None:
            case_name = fromData['case_name']
            case_desc = fromData['case_desc']
            request_address = fromData['request_address']
            if fromData['email_address'] != None:
                email_address = fromData['email_address']
            list_case = []
            for case in fromData['envData']:
                case_env = CaseEnv(project_id=case['pro_id'], modules_id=case['mod_id'], env_id=case['env_id'])
                list_case.append(case_env)

            list_scene = []
            for scene in fromData['sceneData']:
                case_scene = CaseScene(project_id=scene['pro_id'], sceneList_id=scene['scene_id'])
                list_scene.append(case_scene)

            user_case = UserCase(case_name=case_name, case_desc=case_desc, email_address=email_address,
                                 request_address=str(request_address),
                                 case_env=list_case, caseScene=list_scene)
            db.session.add(user_case)
            db.session.commit()
        return jsonify(common.trueReturn('', '用例新增成功'))
    else:
        return jsonify(result)


@case_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    """
    删除Case
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        user_case = UserCase.query.get_or_404(fromData['case_id'])
        db.session.delete(user_case)
        db.session.commit()
        Report.query.filter_by(uc_id=fromData['case_id']).delete(synchronize_session=False)
        db.session.commit()

        CaseScene.query.filter(CaseScene.uc_id == fromData["case_id"]).delete(synchronize_session=False)
        db.session.commit()

        return jsonify(common.trueReturn('', '用例删除成功'))
    else:
        return jsonify(result)


@case_bp.route('/updateCase', methods=['GET', 'POST'])
def updateCase():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        user_case = UserCase.query.get_or_404(fromData['case_id'])
        caseJson = {}
        caseJson['case_name'] = user_case.case_name
        caseJson['case_desc'] = user_case.case_desc
        caseJson['case_id'] = user_case.uc_id
        caseJson['request_address'] = user_case.request_address
        caseJson['email_address'] = user_case.email_address
        case_jsonarray = []
        for case_env in user_case.case_env:
            case_env_dict = {}
            case_env_dict['case_id'] = case_env.case_id
            case_env_dict['env_id'] = case_env.env_id
            env = Environment.query.get_or_404(case_env.env_id)
            case_env_dict['env_name'] = env.env_name
            case_env_dict['mod_id'] = case_env.modules_id
            modules = Modules.query.get_or_404(case_env.modules_id)
            case_env_dict['mod_name'] = modules.modules_name
            case_env_dict['pro_id'] = case_env.project_id
            project = Project.query.get_or_404(case_env.project_id)
            case_env_dict['pro_name'] = project.project_name
            case_jsonarray.append(case_env_dict)
        case_scene_list = []
        for case_scene in user_case.caseScene:
            case_scene_dict = {}
            case_scene_dict['pro_id'] = case_scene.project_id
            project = Project.query.get_or_404(case_scene.project_id)
            case_scene_dict['pro_name'] = project.project_name
            case_scene_dict['scene_id'] = case_scene.sceneList_id
            scene_name = SceneList.query.get_or_404(case_scene.caseScene_id)
            case_scene_dict['scene_name'] = scene_name.scene_name
            case_scene_list.append(case_scene_dict)

        caseJson['case_env_list'] = json.dumps(case_jsonarray, ensure_ascii=False)
        caseJson['case_scene_list'] = json.dumps(case_scene_list, ensure_ascii=False)
        return jsonify(common.trueReturn(caseJson, '用例查询成功'))
    else:
        return jsonify(result)


@case_bp.route('/update', methods=['GET', 'POST'])
def update():
    """
    修改用例
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        if fromData is not None:
            CaseEnv.query.filter(CaseEnv.uc_id == fromData["case_id"]).delete(synchronize_session=False)
            db.session.commit()

            CaseScene.query.filter(CaseScene.uc_id == fromData["case_id"]).delete(synchronize_session=False)
            db.session.commit()
            for case in fromData['envData']:
                case_env = CaseEnv(project_id=case['pro_id'], modules_id=case['mod_id'], env_id=case['env_id'],
                                   uc_id=fromData["case_id"])
                db.session.add(case_env)
                db.session.commit()

            for scene in fromData['sceneData']:
                case_scene = CaseScene(project_id=scene['pro_id'], sceneList_id=scene['scene_id'],uc_id=fromData["case_id"])
                db.session.add(case_scene)
                db.session.commit()

            userCase = UserCase.query.get_or_404(fromData["case_id"])
            userCase.case_name = fromData['case_name']
            userCase.case_desc = fromData['case_desc']
            userCase.request_address = fromData['request_address']
            userCase.email_address = fromData['email_address']
            db.session.commit()
            return jsonify(common.trueReturn('', '修改成功'))
    else:
        return jsonify(result)


@case_bp.route('/start', methods=['GET', 'POST'])
def start():
    """
    启动执行用例
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        report_case_type = str(uuid.uuid1())
        fromData = request.json
        report_create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        test_case(fromData["case_id"], report_case_type, fromData["request_address"], report_create_time)
        strbody = '用例' + str(fromData["case_id"]) + '执行成功'
        execlName = report_case_type.replace('-', '')
        getExecl(report_case_type=report_case_type, execlName=execlName)

        if fromData["email_address"] != None and len(fromData["email_address"]) > 0:
            email_address = fromData["email_address"]
            startPath = os.path.join(current_path, 'logs\\' + execlName + '_interface.xlsx')
            send_mail_with_file(filepath=startPath, filename=u"interface.xlsx", subject=u'接口自动化测试',
                                to_addr=email_address)
        return jsonify(common.trueReturn('', strbody))
    else:
        return jsonify(result)


@case_bp.route('/caseAll', methods=['GET', 'POST'])
def caseAll():
    """
    用例全部查询
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        case = UserCase.query.filter().all()
        case_list = []
        for item in case:
            case_dic = {}
            case_dic['case_id'] = item.uc_id
            case_dic['case_name'] = item.case_name
            case_dic['case_desc'] = item.case_desc
            case_dic['request_address'] = item.request_address
            case_list.append(case_dic)
        list_dic = {}
        list_dic['list'] = case_list

        return jsonify(common.trueReturn(list_dic, '接口查询成功'))
    else:
        return jsonify(result)
