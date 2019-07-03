# -*- coding: utf-8 -*-
"""

"""
from _sha512 import sha512

from interface.models import Project

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='auth.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']


def project_query():
    """
    项目列表查询
    :return:
    """
    try:
        project = Project.query.with_entities(Project.project_id, Project.project_name).all()
        user_dict = []
        for i in project:
            user_dict.append((str(i[0]), i[1]))
        return user_dict
    except BaseException:
        return '项目列表获取异常！'


def getJsonValue(configure, json_body):
    """
    根据用户配置获取配置设置节点的值
    :param configure:
    :param json_body:
    :return:
    """
    configure = configure.split(".")
    # 为了获取b的值
    key = ""
    for i in range(len(configure)):
        key = configure[i]
        if key.isdigit():
            key = int(key)
        json_body = json_body[key]  # 获取到resNum的值

    return json_body


def getRelationship(num):
    """
    校验规则关系
    :param num:
    :return:
    """
    switch = {
        "1": "等于",
        "2": "不等于",
        "3": "包含",
        "4": "不包含",
        "5": "大于",
        "6": "大于等于",
        "7": "小于",
        "8": "小于等于",
        "9": "在列表中",
        "10": "不在列表中"
    }
    return switch[num]


def get_par_type(num):
    """
    参数类型
    :param num:
    :return:
    """
    switch = {
        "0": "String",
        "1": "Number",
        "2": "Date"
    }
    return switch[num]


def get_remote_addr():
    """获取客户端IP地址"""
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if not address:
        address = address.encode('utf-8').split(b',')[0].strip()
    return address


def create_browser_id():
    agent = request.headers.get('User-Agent')
    if not agent:
        agent = str(agent).encode('utf-8')
    base_str = "%s|%s" % (get_remote_addr(), agent)
    h = sha512()
    h.update(base_str.encode('utf8'))
    return h.hexdigest()


def txt_wrap_by(start_str, end, html):
    """
    取两个字符之间的内容
    :param start_str:
    :param end:
    :param html:
    :return:
    """
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
