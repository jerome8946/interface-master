# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, current_app
import json
import math

from interface import Auth, db, common
from interface.models import SceneList, Project, SceneEnv, HeaderValue, Check, Variable, Environment

scene_bp = Blueprint('scene', __name__, url_prefix='/scene', static_folder='static')


@scene_bp.route('/', methods=['GET', 'POST'])
@scene_bp.route('/index', methods=['GET', 'POST'])
@scene_bp.route('/index/<int:page>', methods=['GET', 'POST'])
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
        project_name = fromData['proname']
        scenename = fromData['scenename']
        # 拼接查询条件
        stmt = Project.query.with_entities(Project.project_id).filter(
            Project.project_name.like("%" + project_name + "%")).subquery()
        if scenename != 'None' and len(scenename) > 0:
            param.append(SceneList.scene_name.like("%" + scenename + "%"))

        # 每页显示数
        per_page = current_app.config['INTERFACE_PER_PAGE']
        # 分页对象
        pagination = db.session.query(SceneList).join(stmt, SceneList.project_id == stmt.c.project_id).filter(
            *param).group_by(SceneList.sceneList_id).paginate(
            page,
            per_page=per_page)

        # 总条数
        count = db.session.query(SceneList).join(stmt, SceneList.project_id == stmt.c.project_id).filter(
            *param).group_by(SceneList.sceneList_id).count()
        # # 总页数
        page_count = math.ceil(count / per_page)

        # 当前页数的记录列表
        sceneList = pagination.items
        scene_list = []
        for item in sceneList:
            scene_dic = {}
            scene_dic['sceneList_id'] = item.sceneList_id
            scene_dic['scene_name'] = item.scene_name
            scene_dic['project_id'] = item.project_id
            project = Project.query.with_entities(Project.project_name).filter(
                Project.project_id == item.project_id).all()
            scene_dic['project_name'] = project[0].project_name

            scene_dic['scene_desc'] = item.scene_desc
            scene_list.append(scene_dic)

        list_dic = {}
        list_dic['list'] = scene_list
        list_dic['count'] = count
        list_dic['page_count'] = page_count
        list_dic['per_page'] = per_page
        return jsonify(common.trueReturn(list_dic, '场景查询成功'))
    else:
        return jsonify(result)


@scene_bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    模块接口
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:

        sceneList = request.json.get("sceneList")

        list_sceneEnvData = []
        index_num = 1
        for sceneEnvData in sceneList['sceneEnvData']:
            list_header = []
            for headerData in sceneEnvData['headerData']:
                herader = HeaderValue(header_name=headerData['header_name'], header_value=headerData['header_value'])
                list_header.append(herader)
            list_check = []
            check = Check(check_verification_code=sceneEnvData['check_body']['check_verification_code'],
                          check_agreement_relation=sceneEnvData['check_body']['check_agreement_relation'],
                          check_verification_value=sceneEnvData['check_body']['check_verification_value'])
            list_check.append(check)

            variableList = []
            for var in sceneEnvData['variableData']:
                variable = Variable(var_regexp=var['var_regexp'], var_name=var['var_name'])
                variableList.append(variable)

            sceneEnv = SceneEnv(project_id=sceneEnvData['project_id'], modules_id=sceneEnvData['modules_id'],
                                env_id=sceneEnvData['env_id'], scene_body=sceneEnvData['bodyData'], header=list_header,
                                check=list_check, variable=variableList, number=index_num)
            index_num += 1
            list_sceneEnvData.append(sceneEnv)

        sceneList = SceneList(scene_name=sceneList['scene_name'], project_id=sceneList['project_id'],
                              scene_desc=sceneList['scene_desc'], sceneEnv=list_sceneEnvData)

        db.session.add(sceneList)
        db.session.commit()

        return jsonify(common.trueReturn('', '场景新增成功'))
    else:
        return jsonify(result)


@scene_bp.route('/selectUpdat', methods=['GET', 'POST'])
def selectUpdat():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        sceneList_id = request.json.get('sceneList_id')
        sceneList = SceneList.query.get_or_404(sceneList_id)
        sceneJson = {}
        sceneJson['scene_name'] = sceneList.scene_name
        sceneJson['project_id'] = sceneList.project_id
        sceneJson['scene_desc'] = sceneList.scene_desc
        sceneEnvData = []
        for sceneEnv in sceneList.sceneEnv:
            scene = {}
            scene['scene_id'] = sceneEnv.scene_id
            scene['project_id'] = sceneEnv.project_id
            scene['modules_id'] = sceneEnv.modules_id
            scene['env_id'] = sceneEnv.env_id
            env = Environment.query.filter(
                Environment.env_id == sceneEnv.env_id).all()
            scene['env_name'] = env[0].env_name
            scene['project_name'] = env[0].project.project_name
            scene['modules_name'] = env[0].modules.modules_name
            scene['bodyData'] = sceneEnv.scene_body
            headerData = []
            for sceneHeader in sceneEnv.header:
                header = {}
                header['header_name'] = sceneHeader.header_name
                header['header_value'] = sceneHeader.header_value
                header['header_id'] = sceneHeader.header_id
                headerData.append(header)
            scene['headerData'] = headerData
            check_body = {}
            check_body['check_verification_code'] = sceneEnv.check[0].check_verification_code
            check_body['check_agreement_relation'] = sceneEnv.check[0].check_agreement_relation
            check_body['check_verification_value'] = sceneEnv.check[0].check_verification_value
            scene['check_body'] = check_body

            variableData = []
            for sceneVariable in sceneEnv.variable:
                variable = {}
                variable['var_regexp'] = sceneVariable.var_regexp
                variable['var_id'] = sceneVariable.var_id
                variable['var_name'] = sceneVariable.var_name
                variable['var_value'] = sceneVariable.var_value
                variableData.append(variable)
            scene['variableData'] = variableData
            sceneEnvData.append(scene)

        sceneJson['sceneEnvData'] = sceneEnvData

        return jsonify(common.trueReturn(sceneJson, '查询成功'))
    else:
        return jsonify(result)


@scene_bp.route('/update', methods=['GET', 'POST'])
def update():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json.get("sceneList")
        scene_id_All = SceneEnv.query.with_entities(SceneEnv.scene_id).filter(
            SceneEnv.sceneList_id == fromData["sceneList_id"]).all()
        for scene in scene_id_All:
            # 删除数据
            checkList = Check.query.filter(Check.scene_id == scene.scene_id).first()
            if checkList is not None:
                Check.query.filter(Check.scene_id == scene.scene_id).delete(synchronize_session=False)
                db.session.commit()

            headerList = HeaderValue.query.filter(HeaderValue.scene_id == scene.scene_id).first()
            if headerList is not None:
                HeaderValue.query.filter(HeaderValue.scene_id == scene.scene_id).delete(synchronize_session=False)
                db.session.commit()

            variableList = Variable.query.filter(Variable.scene_id == scene.scene_id).first()
            if variableList is not None:
                Variable.query.filter(Variable.scene_id == scene.scene_id).delete(synchronize_session=False)
                db.session.commit()

            sceneEnvList = SceneEnv.query.filter(SceneEnv.scene_id == scene.scene_id).first()
            if sceneEnvList is not None:
                SceneEnv.query.filter(SceneEnv.scene_id == scene.scene_id).delete(synchronize_session=False)
                db.session.commit()
        index_num = 1
        for sceneEnvData in fromData['sceneEnvData']:
            list_header = []
            for headerData in sceneEnvData['headerData']:
                herader = HeaderValue(header_name=headerData['header_name'], header_value=headerData['header_value'])
                list_header.append(herader)
            list_check = []
            check = Check(check_verification_code=sceneEnvData['check_body']['check_verification_code'],
                          check_agreement_relation=sceneEnvData['check_body']['check_agreement_relation'],
                          check_verification_value=sceneEnvData['check_body']['check_verification_value'])
            list_check.append(check)

            variableList = []
            for var in sceneEnvData['variableData']:
                variable = Variable(var_regexp=var['var_regexp'], var_name=var['var_name'])
                variableList.append(variable)

            sceneEnv = SceneEnv(project_id=sceneEnvData['project_id'], modules_id=sceneEnvData['modules_id'],
                                env_id=sceneEnvData['env_id'], scene_body=sceneEnvData['bodyData'], header=list_header,
                                check=list_check, variable=variableList, sceneList_id=fromData["sceneList_id"],
                                number=index_num)
            db.session.add(sceneEnv)
            db.session.commit()
            index_num += 1

        sceneList = SceneList.query.get_or_404(fromData["sceneList_id"])
        sceneList.scene_name = fromData['scene_name']
        sceneList.project_id = fromData['project_id']
        sceneList.scene_desc = fromData['scene_desc']
        db.session.commit()

        return jsonify(common.trueReturn('', '场景编辑成功'))
    else:
        return jsonify(result)


@scene_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        sceneList_id = request.json.get('sceneList_id')
        SceneList.query.filter_by(sceneList_id=sceneList_id).delete()
        db.session.commit()

        scene_id_All = SceneEnv.query.with_entities(SceneEnv.scene_id).filter(
            SceneEnv.sceneList_id == sceneList_id).all()
        for scene in scene_id_All:
            # 删除数据
            checkList = Check.query.filter(Check.scene_id == scene.scene_id).first()
            if checkList is not None:
                Check.query.filter(Check.scene_id == scene.scene_id).delete(synchronize_session=False)
                db.session.commit()

            headerList = HeaderValue.query.filter(HeaderValue.scene_id == scene.scene_id).first()
            if headerList is not None:
                HeaderValue.query.filter(HeaderValue.scene_id == scene.scene_id).delete(synchronize_session=False)
                db.session.commit()

            variableList = Variable.query.filter(Variable.scene_id == scene.scene_id).first()
            if variableList is not None:
                Variable.query.filter(Variable.scene_id == scene.scene_id).delete(synchronize_session=False)
                db.session.commit()

            sceneEnvList = SceneEnv.query.filter(SceneEnv.scene_id == scene.scene_id).first()
            if sceneEnvList is not None:
                SceneEnv.query.filter(SceneEnv.scene_id == scene.scene_id).delete(synchronize_session=False)
                db.session.commit()

        return jsonify(common.trueReturn('', '场景删除成功'))
    else:
        return jsonify(result)


@scene_bp.route('/selectSceneList', methods=['GET', 'POST'])
def select_modular():
    """
    根据项目查询场景
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        project_id = fromData['project_id']
        model = SceneList.query.with_entities(SceneList.sceneList_id, SceneList.scene_name).filter(
            SceneList.project_id == project_id).all()
        sceneList_dict = []
        for p, k in model:
            sceneList_json = {}
            sceneList_json['sceneList_id'] = p
            sceneList_json['scene_name'] = k
            sceneList_dict.append(sceneList_json)
        return jsonify(common.trueReturn(sceneList_dict, '场景查询成功'))
    else:
        return jsonify(result)
