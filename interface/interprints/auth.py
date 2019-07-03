# -*- coding: utf-8 -*-
import datetime
import os
import time

import jwt
from flask import Blueprint, request, abort, jsonify

from interface import common, db
from interface.models import Admin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', static_folder='static')


# @auth_bp.after_request
# def after_request(response):
#     # 调用函数生成 csrf_token
#     csrf_token = generate_csrf()
#     # # 通过 cookie 将值传给前端
#     # session['csrf_token']=csrf_token
#     # response.set_cookie("csrf_token", csrf_token)
#     # return response
#     # 设置cookie  cookie名 cookie值 默认临时cookie浏览器关闭即失效
#     # 通过max_age控制cookie有效期, 单位:秒
#     response.set_cookie("csrf_token", csrf_token, max_age=3600)
#     session['csrf_token'] = csrf_token
#     # response.headers["csrf_token"] = csrf_token
#     return response
#
#
# @auth_bp.route('/')
# @login_required
# def index():
#     form = ModulesAddForm()
#     return render_template('modular/add_modular.html', form=form)
#
#
@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    else:
        return Auth.authenticate(Auth, username, password)


#
#
# @auth_bp.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Logout success.', 'info')
#     return redirect_back()


class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET_KEY', 'dev key'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, os.getenv('SECRET_KEY', 'dev key'), options={'verify_exp': False})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        admin = Admin.query.filter_by(username=username).first()
        if admin is None:
            return jsonify(common.falseReturn('', '找不到用户'))
        else:
            if username == admin.username and admin.validate_password(password):
                login_time = int(time.time())
                admin.login_time = login_time
                db.session.commit()
                token = self.encode_auth_token(admin.id, login_time)
                return jsonify(common.trueReturn(token.decode(), '登录成功'))
            else:
                return jsonify(common.falseReturn('', '密码不正确'))

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
                result = common.falseReturn('', '请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = Admin.get(Admin, payload['data']['id'])
                    if user is None:
                        result = common.falseReturn('', '找不到该用户信息')
                    else:
                        if user.login_time == payload['data']['login_time']:
                            result = common.trueReturn(user.id, '请求成功')
                        else:
                            result = common.falseReturn('', 'Token已更改，请重新登录获取')
                else:
                    result = common.falseReturn('', payload)
        else:
            result = common.falseReturn('', '没有提供认证token')
        return result
