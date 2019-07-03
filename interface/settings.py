# -*- coding: utf-8 -*-

import os
import sys

# 返回脚本的路径
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    # 配置一个加密密钥
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    # DEBUG是否拦截重定向
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # 该配置为True,则每次请求结束都会自动commit数据库的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CSRF_ENABLED = True

    # 为图片上传请求添加 CSRF 保护
    CKEDITOR_ENABLE_CSRF = True

    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('port Admin', MAIL_USERNAME)
    # # 每页数量
    INTERFACE_PER_PAGE = 10
    # ('theme name', 'display name')

    BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    BLUELOG_SLOW_QUERY_THRESHOLD = 1
    # 处理上传文件的URL或端点
    BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    # 限制上传格式
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
