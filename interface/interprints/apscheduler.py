# -*- coding: utf-8 -*-
import datetime
import json
import math

from flask import Blueprint, request, jsonify, current_app, url_for, redirect

from interface import common, appInster
from interface.interprints.auth import Auth
from interface.extensions import scheduler, db
from interface.mock.implement import test_caseList
from interface.models import Scheduling, UserCase, TaskCase, Report
import uuid

aps_bp = Blueprint('aps', __name__, url_prefix='/aps', static_folder='static')



def pausetask(id):
    """
    暂停
    :return:
    """
    print("暂停的id  "+id)
    get_task()
    scheduler.pause_job(str(id))


def resumetask(id):
    """
    恢复任务
    :return:
    """
    scheduler._scheduler.resume_job(str(id))


@aps_bp.route('/gettask', methods=['GET,POST'])
def get_task():
    """
    获取任务
    :return:
    """
    jobs = scheduler.get_jobs()
    print(jobs)
    return '111'


@aps_bp.route('/remove_task', methods=['POST'])
def remove_task(id):
    """
    删除任务
    :return:
    """
    scheduler.remove_job(str(id))
    # registerAllTask()

def addtask(fromData, id):
    """
    添加任务
    :return:
    """
    try:
        caseList = fromData['caseList']
        cronStr = fromData['scheduling_cron']
        email_address = fromData['email_address']
        cronStr = cronStr.replace("?", "*")
        cronStr = cronStr.split(" ")
        day = str(cronStr[3])
        if day == '0':
            day = '*'
        month = str(cronStr[4])
        if month == '0':
            month = '*'

        week = str(cronStr[5])
        if week == '0':
            week = '*'

        second = str(cronStr[0])
        minute = str(cronStr[1])
        hour = str(cronStr[2])

        if len(cronStr) == 6:
            year = str(cronStr[6])
        else:
            year = '*'

        scheduler.add_job(func=test_caseList, id=id,
                          kwargs={'caseList': caseList, 'scheduling_id': id, 'email_address': email_address},
                          trigger='cron',
                          second=second,
                          minute=minute,
                          hour=hour,
                          day=day, month=month, day_of_week=week, year=year,
                          replace_existing=True)
    except Exception as e:
        print('出异常 ', e)
        Scheduling.query.filter_by(scheduling_id=id).delete(synchronize_session=False)
        db.session.commit()
        TaskCase.query.filter(TaskCase.scheduling_id == id).delete(synchronize_session=False)
        db.session.commit()


@aps_bp.route('/addjob', methods=['POST'])
def addjob():
    """
    添加任务
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:

        fromData = request.json
        caseList = fromData['caseList']
        cronStr = fromData['scheduling_cron']
        scheduling_title = fromData['scheduling_title']
        email_address = fromData['email_address']
        cronStr = cronStr.replace("?", "*")
        cronStrValue = cronStr
        id = str(uuid.uuid1()).replace('-','')
        scheduling = Scheduling(scheduling_id=id, scheduling_title=scheduling_title,
                                scheduling_cron=str(cronStrValue),
                                scheduling_on='0', email_address=email_address)
        db.session.add(scheduling)
        db.session.commit()
        for case in caseList:
            taskCase = TaskCase(scheduling_id=id, case_id=case['case_id'])
            db.session.add(taskCase)
            db.session.commit()
        addtask(fromData, id)
        return jsonify(common.trueReturn('', '任务新增成功'))
    else:
        return jsonify(result)


@aps_bp.route('/index', methods=['GET', 'POST'])
def index():
    """
    任务查询
    :param page: 页数
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = json.loads(request.args['0'])
        page = fromData['page']
        param = []
        # 拼接查询条件
        if fromData['scheduling_title'] != 'None' and len(fromData['scheduling_title']) > 0:
            param.append(Scheduling.scheduling_title.like("%" + fromData['scheduling_title'] + "%"))

        # 每页显示数
        per_page = current_app.config['INTERFACE_PER_PAGE']
        # 分页对象
        pagination = Scheduling.query.filter(*param).paginate(page, per_page=per_page)

        # 总条数
        count = Scheduling.query.filter(*param).count()
        # # 总页数
        page_count = math.ceil(count / per_page)
        # print('总页数 ', page_count)
        # 当前页数的记录列表
        schedulingList = pagination.items
        scheduling_list = []
        for item in schedulingList:
            scheduling_dic = {}
            scheduling_dic['scheduling_id'] = item.scheduling_id
            scheduling_dic['scheduling_title'] = item.scheduling_title
            scheduling_dic['scheduling_cron'] = item.scheduling_cron
            scheduling_dic['scheduling_on'] = item.scheduling_on
            scheduling_dic['email_address'] = item.email_address
            scheduling_list.append(scheduling_dic)
        list_dic = {}
        list_dic['list'] = scheduling_list
        list_dic['count'] = count
        list_dic['page_count'] = page_count
        list_dic['per_page'] = per_page
        get_task()
        return jsonify(common.trueReturn(list_dic, '任务查询成功'))
    else:
        return jsonify(result)


@aps_bp.route('/updateAps', methods=['GET', 'POST'])
def updateAps():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        scheduling = Scheduling.query.get_or_404(fromData['scheduling_id'])
        schedulingJson = {}
        schedulingJson['scheduling_id'] = scheduling.scheduling_id
        schedulingJson['scheduling_title'] = scheduling.scheduling_title
        schedulingJson['scheduling_on'] = scheduling.scheduling_on
        schedulingJson['scheduling_cron'] = scheduling.scheduling_cron
        schedulingJson['email_address'] = scheduling.email_address
        taskCaseList = TaskCase.query.filter(TaskCase.scheduling_id == fromData["scheduling_id"]).all()
        task_jsonarray = []
        for task in taskCaseList:
            task_dict = {}
            task_dict['task_id'] = task.task_id
            task_dict['case_id'] = task.case_id
            user_case = UserCase.query.get_or_404(task.case_id)
            task_dict['scheduling_id'] = task.scheduling_id
            task_dict['case_name'] = user_case.case_name
            task_dict['request_address'] = user_case.request_address
            task_jsonarray.append(task_dict)
        schedulingJson['caseData'] = task_jsonarray

        return jsonify(common.trueReturn(schedulingJson, '任务查询成功'))
    else:
        return jsonify(result)


@aps_bp.route('/update', methods=['GET', 'POST'])
def update():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        scheduling = Scheduling.query.get_or_404(fromData['scheduling_id'])
        scheduling.scheduling_title = fromData['scheduling_title']
        scheduling.scheduling_cron = fromData['scheduling_cron']
        scheduling.email_address = fromData['email_address']
        db.session.commit()
        taskList = fromData['caseList']
        TaskCase.query.filter(TaskCase.scheduling_id == fromData["scheduling_id"]).delete(synchronize_session=False)
        db.session.commit()
        for task in taskList:
            taskCase = TaskCase(scheduling_id=fromData['scheduling_id'], case_id=task['case_id'])
            db.session.add(taskCase)
            db.session.commit()
        # 删除任务
        remove_task(fromData['scheduling_id'])
        # 添加任务
        addtask(fromData, fromData['scheduling_id'])

        return jsonify(common.trueReturn('', '修改成功'))
    else:
        return jsonify(result)


@aps_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    """
    删除任务
    :return:
    """
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        Scheduling.query.filter_by(scheduling_id=fromData["scheduling_id"]).delete(synchronize_session=False)
        db.session.commit()
        TaskCase.query.filter(TaskCase.scheduling_id == fromData["scheduling_id"]).delete(synchronize_session=False)
        db.session.commit()
        get_task()
        print(fromData["scheduling_id"])
        remove_task(fromData["scheduling_id"])
        return jsonify(common.trueReturn('', '删除成功'))
    else:
        return jsonify(result)


def registerAllTask():
    """
    添加所有的任务
    :return:
    """
    schedulingList = Scheduling.query.filter().all()
    fromData = {}
    for scheduling in schedulingList:
        fromData['scheduling_id'] = scheduling.scheduling_id
        fromData['scheduling_cron'] = scheduling.scheduling_cron
        fromData['email_address'] = scheduling.email_address
        taskCaseList = TaskCase.query.filter(TaskCase.scheduling_id == fromData["scheduling_id"]).all()
        caseList = []
        for task in taskCaseList:
            # caseList.append(task.case_id)
            case_id = {}
            case_id['case_id'] = task.case_id
            caseList.append(case_id)
        fromData['caseList'] = caseList
        addtask(fromData, scheduling.scheduling_id)
        if scheduling.scheduling_on == 1:
            scheduler.pause_job(scheduling.scheduling_id)







@aps_bp.route('/pause', methods=['GET', 'POST'])
def pause():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        pausetask(fromData["scheduling_id"])
        scheduling = Scheduling.query.get_or_404(fromData['scheduling_id'])
        scheduling.scheduling_on = '1'
        db.session.commit()
        return jsonify(common.trueReturn('', '暂停任务'))
    else:
        return jsonify(result)


@aps_bp.route('/resume', methods=['GET', 'POST'])
def resume():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        resumetask(fromData["scheduling_id"])
        scheduling = Scheduling.query.get_or_404(fromData['scheduling_id'])
        scheduling.scheduling_on = '0'
        db.session.commit()
        return jsonify(common.trueReturn('', '恢复任务'))
    else:
        return jsonify(result)


@aps_bp.route('/startExecution', methods=['GET', 'POST'])
def startExecution():
    result = Auth.identify(Auth, request)
    if result['status'] and result['data']:
        fromData = request.json
        taskCaseList = TaskCase.query.filter(TaskCase.scheduling_id == fromData["scheduling_id"]).all()
        task_jsonarray = []
        for task in taskCaseList:
            task_dict = {}
            task_dict['task_id'] = task.task_id
            task_dict['case_id'] = task.case_id
            user_case = UserCase.query.get_or_404(task.case_id)
            task_dict['scheduling_id'] = task.scheduling_id
            task_dict['case_name'] = user_case.case_name
            task_dict['request_address'] = user_case.request_address
            task_jsonarray.append(task_dict)
            # 删除该调度日志
        test_caseList(task_jsonarray, fromData["scheduling_id"], email_address=fromData["email_address"])
        return jsonify(common.trueReturn('', '执行完成'))
    else:
        return jsonify(result)


def task1(a, b):
    print('mession1')
    print(datetime.datetime.now())

def addtasktest():
    scheduler.add_job(func=task1, id='87085108-8833-11e9-98a4-1062e5516e84', args=(1, 2), trigger='cron', second='*', minute='0/1', hour='*',
                          day='*', month='*', week='*', year='*',
                          replace_existing=True)

