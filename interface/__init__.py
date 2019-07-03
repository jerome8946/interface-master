# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_jwt import JWT
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from interface.extensions import bootstrap, db, ckeditor, mail, moment, toolbar, migrate, scheduler
from interface.interprints.apscheduler import aps_bp
from interface.interprints.auth import auth_bp, Auth
from interface.interprints.environment import env_bp
from interface.interprints.modular import modular_bp
from interface.interprints.project import poj_bp
from interface.interprints.reportLog import report_bp
from interface.interprints.scene import scene_bp
from interface.interprints.usercase import case_bp

from interface.models import Admin, Project, Modules, Environment, Parameter, Variable, Transfer, UserCase, CaseEnv, \
    Report, Scheduling, TaskCase, SceneEnv
from interface.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))



def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('interface')
    app.config.from_object(config[config_name])
    CORS(app, supports_credentials=True, resources=r'/*')
    auth = Auth()
    JWT(app, auth.authenticate, auth.identify)
    # 注册日志处理
    register_logging(app)
    # 注册扩展(初始化）
    register_extensions(app)
    # 注册蓝本
    register_blueprints(app)
    # 注册自定义shell命令
    register_commands(app)
    # 注册错误处理函数
    register_errors(app)
    # 注册shell 上下文处理函数
    register_shell_context(app)
    # 注册模板上下文处理函数
    register_template_context(app)
    register_request_handlers(app)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/interface.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Interface Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    # login_manager.init_app(app)
    # csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(poj_bp, url_prefix='/project')
    app.register_blueprint(modular_bp, url_prefix='/modular')
    app.register_blueprint(env_bp, url_prefix='/env')
    app.register_blueprint(case_bp, url_prefix='/case')
    app.register_blueprint(aps_bp, url_prefix='/aps')
    app.register_blueprint(report_bp, url_prefix='/report')
    app.register_blueprint(scene_bp, url_prefix='/scene')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Project=Project, Modules=Modules, Environment=Environment, Parameter=Parameter,
                    Transfer=Transfer, Variable=Variable, UserCase=UserCase, CaseEnv=CaseEnv, Report=Report,
                    Scheduling=Scheduling, TaskCase=TaskCase,SceneEnv=SceneEnv)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        project = Project.query.first()
        modules = Modules.query.first()
        env = Environment.query.first()
        par = Parameter.query.first()
        tra = Transfer.query.first()
        var = Variable.query.first()
        usercase = UserCase.query.first()
        caseenv = CaseEnv.query.first()
        report = Report.query.first()
        scheduling = Scheduling.query.first()
        taskCase = TaskCase.query.first()
        sceneEnv = SceneEnv.query.first()
        return dict(
            admin=admin, project=project, modules=modules, env=env, par=par, tra=tra, var=var, usercase=usercase,
            caseenv=caseenv, report=report, scheduling=scheduling, taskCase=taskCase, sceneEnv=sceneEnv)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('确定清除数据吗?', abort=True)
            db.drop_all()
            click.echo('清空数据完成.')
        db.create_all()
        click.echo('重新创建表格.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='请输入账号.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='请输入密码.')
    def init(username, password):
        """Building Interface, just for you."""

        click.echo('创建表格...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('管理员已存在正在更新...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('创建临时管理员账户...')
            admin = Admin(
                username=username,
                name='Admin',
            )
            admin.set_password(password)
            db.session.add(admin)

            project = Project.query.first()
        if project is None:
            click.echo('创建默认项目...')
            project = Project(
                project_name='Default',
                project_desc='Default',
                status='1'
            )
            db.session.add(project)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--project', default=5, help='Quantity of project, default is 10.')
    @click.option('--modules', default=20, help='Quantity of modules, default is 50.')
    def forge(project, modules):
        """Generate fake data."""
        from interface.fakes import fake_admin, fake_project, fake_modules

        db.drop_all()
        db.create_all()

        click.echo('创建用户表数据...')
        fake_admin()

        # click.echo('创建 %d 项目...' % project)
        # fake_project(project)
        #
        # click.echo('创建 %d 模块...' % modules)
        # fake_modules(modules)

        click.echo('Done.')


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response
