# -*- coding: utf-8 -*-
import json
import math
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from flask import Blueprint, redirect, url_for, flash, request, current_app, jsonify, make_response, send_file, \
    send_from_directory

from interface.interprints.auth import Auth, common, db
from interface.HandleExcel import HandleExcel

from interface.models import Report, UserCase

current_path = os.path.abspath('.')
report_bp = Blueprint('report', __name__, url_prefix='/report', static_folder='static')


@report_bp.route('/getReport', methods=['GET', 'POST'])
def getReport():
    """
    查询case报告
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        case_id = fromData['case_id']
        page = fromData['page']
        param = [Report.uc_id == case_id]
        try:
            param.append(Report.report_case_type == fromData['report_case_type'])
        except Exception as e:
            report = Report.query.with_entities(Report.report_create_time, Report.report_case_type).filter(
                Report.uc_id == case_id).order_by(
                Report.report_create_time.desc()).first()
            param.append(Report.report_case_type == report.report_case_type)
            # param.append(Report.report_create_time == report.report_create_time)
        # 拼接查询条件
        if fromData['report_url'] != 'None' and len(fromData['report_url']) > 0:
            param.append(Report.report_url.like("%" + fromData['report_url'] + "%"))
        if fromData['report_env_pass'] != 'None' and len(fromData['report_env_pass']) > 0:
            param.append(Report.report_env_pass == fromData['report_env_pass'])
        # 每页显示数
        per_page = 5
        # 分页对象
        pagination = Report.query.filter(*param).paginate(page, per_page=per_page)

        # 总条数
        count = Report.query.filter(*param).count()
        # # 总页数
        page_count = math.ceil(count / per_page)
        # print('总页数 ', page_count)
        # 当前页数的记录列表
        reportList = pagination.items
        report_dict = []
        for report in reportList:
            report_json = {}
            report_json['report_id'] = report.report_id
            report_json['report_title'] = report.report_title
            report_json['report_url'] = report.report_url
            report_json['report_env_param'] = report.report_env_param
            report_json['report_env_status'] = report.report_env_status
            report_json['report_env_time'] = report.report_env_time
            report_json['report_env_response'] = report.report_env_response
            report_json['report_env_pass'] = report.report_env_pass
            report_dict.append(report_json)
        list_dic = {}
        list_dic['list'] = report_dict
        list_dic['count'] = count
        list_dic['page_count'] = page_count
        list_dic['per_page'] = per_page
        return jsonify(common.trueReturn(list_dic, '日志查询成功'))
    else:
        return jsonify(result)


@report_bp.route('/getReportList', methods=['GET', 'POST'])
def getReportList():
    """
    查询case报告列表
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        case_id = fromData['case_id']
        # page = fromData['page']
        param = [Report.uc_id == case_id]
        # 拼接查询条件
        # 每页显示数
        # per_page = 5
        # 分页对象
        # pagination = Report.query.filter(*param).group_by(Report.report_case_type).order_by(
        #     Report.report_create_time).paginate(page, per_page=per_page)
        # # 总条数
        # count = Report.query.filter(*param).group_by(Report.report_case_type).count()
        # # # 总页数
        # page_count = math.ceil(count / per_page)
        # # print('总页数 ', page_count)
        # # 当前页数的记录列表
        # reportList = pagination.items
        reportList = Report.query.filter(*param).group_by(Report.report_case_type).order_by(
            Report.report_create_time.desc()).all()
        report_dict = []
        for report in reportList:
            report_json = {}
            report_json['report_id'] = report.report_id
            report_json['report_title'] = report.report_title
            report_json['report_case_type'] = report.report_case_type
            report_json['report_create_time'] = report.report_create_time
            report_json['case_id'] = report.uc_id
            report_dict.append(report_json)
        list_dic = {}
        list_dic['list'] = report_dict
        # list_dic['count'] = count
        # list_dic['page_count'] = page_count
        # list_dic['per_page'] = per_page

        return jsonify(common.trueReturn(list_dic, '日志列表查询成功'))
    else:
        return jsonify(result)


@report_bp.route('/deleteType', methods=['GET', 'POST'])
def deleteType():
    """
    删除case
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        report_case_type = request.json.get('report_case_type')
        Report.query.filter_by(report_case_type=report_case_type).delete(synchronize_session=False)
        db.session.commit()
        return jsonify(common.trueReturn('', '日志删除成功'))
    else:
        return jsonify(result)


@report_bp.route('/getLogCaseList', methods=['GET', 'POST'])
def getLogCaseList():
    """
    case列表
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        param = [Report.scheduling_id == fromData['scheduling_id']]
        reporteList = Report.query.filter(*param).group_by(Report.uc_id).order_by(
            Report.report_create_time.desc()).all()
        caseList = []
        log_case_pass = 0
        for report in reporteList:
            case = {}
            user_case = UserCase.query.get_or_404(report.uc_id)
            case['log_case_name'] = user_case.case_name
            case['log_case_id'] = user_case.uc_id
            casePass = [Report.report_env_pass == '1', Report.uc_id == report.uc_id]
            casePass = Report.query.filter(*casePass).all()
            if len(casePass) > 0:
                log_case_pass = 1
            else:
                log_case_pass =0
            case['log_case_pass'] = log_case_pass
            caseList.append(case)
        # vueExecl 表格下载
        loadCaseList = getLoadCaseList(fromData['scheduling_id'])

        resBody = {}
        resBody['caseList'] = caseList
        resBody['loadCaseList'] = loadCaseList
        return jsonify(common.trueReturn(resBody, '日志列表查询成功'))
    else:
        return jsonify(result)


@report_bp.route('/getReportCaseList', methods=['GET', 'POST'])
def getReportCaseList():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        casePass = [Report.uc_id == fromData['case_id'], Report.scheduling_id == fromData['scheduling_id']]
        reportList = Report.query.filter(*casePass).all()
        report_dict = []
        for report in reportList:
            report_json = {}
            report_json['report_id'] = report.report_id
            report_json['report_title'] = report.report_title
            report_json['report_url'] = report.report_url
            report_json['report_env_param'] = report.report_env_param
            report_json['report_env_status'] = report.report_env_status
            report_json['report_env_time'] = report.report_env_time
            report_json['report_env_response'] = report.report_env_response
            report_json['report_env_pass'] = report.report_env_pass
            report_dict.append(report_json)

        return jsonify(common.trueReturn(report_dict, '日志列表查询成功'))
    else:
        return jsonify(result)


def deleteScheduling(scheduling_id):
    """
    删除调度日志
    :return:
    """
    Report.query.filter_by(scheduling_id=scheduling_id).delete(synchronize_session=False)
    db.session.commit()


def getLoadCaseList(scheduling_id):
    casePass = [Report.scheduling_id == scheduling_id]
    reportList = Report.query.filter(*casePass).all()
    report_dict = []
    for report in reportList:
        report_json = {}
        report_json['report_id'] = report.report_id
        report_json['report_title'] = report.report_title
        report_json['report_url'] = report.report_url
        report_json['report_env_param'] = report.report_env_param
        report_json['report_env_status'] = report.report_env_status
        report_json['report_env_time'] = report.report_env_time
        report_json['report_env_response'] = report.report_env_response
        report_json['report_env_pass'] = report.report_env_pass
        report_dict.append(report_json)
    return report_dict


def getExecl(report_case_type='', execlName='', scheduling_id=''):
    if report_case_type != '':
        param = [Report.report_case_type == report_case_type]

    if scheduling_id != '':
        param = [Report.scheduling_id == scheduling_id]

    reportList = Report.query.filter(*param).all()
    startPath = os.path.join(current_path, 'logs\\' + execlName + '_interface.xlsx')
    handExcel = HandleExcel(file=startPath, sheet_id=0)
    handExcel.write_value(startPath, 1, 1, '标题')
    handExcel.write_value(startPath, 1, 2, '请求地址')
    handExcel.write_value(startPath, 1, 3, '请求参数')
    handExcel.write_value(startPath, 1, 4, '响应状态')
    handExcel.write_value(startPath, 1, 5, '响应时间')
    handExcel.write_value(startPath, 1, 6, '响应内容')
    handExcel.write_value(startPath, 1, 7, '是否通过')
    i = 2
    report_dict = []
    for report in reportList:
        for num in range(1, 7):
            report_json = {}
            report_json['row'] = i
            report_json['col'] = num
            report_json['valuePass'] = report.report_env_pass
            if num == 1:
                report_json['value'] = report.report_title
            elif num == 2:
                report_json['value'] = report.report_url
            elif num == 3:
                report_json['value'] = report.report_env_param
            elif num == 4:
                report_json['value'] = report.report_env_status
            elif num == 5:
                report_json['value'] = report.report_env_time
            elif num == 6:
                report_json['value'] = report.report_env_response
            elif num == 7:
                env_pass = '不通过'
                if report.report_env_pass == 0:
                    env_pass = '通过'
                report_json['value'] = env_pass
            report_dict.append(report_json)
        i += 1

    handExcel.write_value_all(path=startPath, allList=report_dict)
