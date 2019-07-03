# -*- coding: utf-8 -*-
"""
生成虚拟数据

"""
from sqlalchemy.exc import IntegrityError
import random

from faker import Faker

from interface import Admin, db
from interface.models import Project, Modules, Environment, Parameter, Transfer, Variable

fake = Faker()


# 管理员
def fake_admin():
    admin = Admin(
        username='admin',
        name='Admin',

    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()


# 项目名称
def fake_project(count=2):
    project = Project(project_name='Default', project_desc='Default',
                      status='1')
    db.session.add(project)

    for i in range(count):
        project = Project(
            project_name=fake.word(),
            project_desc=fake.text(100)
        )
        db.session.add(project)
        try:
            # 提交
            db.session.commit()
        except IntegrityError:
            # 回滚
            db.session.rollback()


# 模块管理
def fake_modules(count=10):
    for i in range(count):
        modules = Modules(
            modules_name=fake.word(),
            modules_desc=fake.text(50),
            project=Project.query.get(random.randint(1, Project.query.count()))
        )
        db.session.add(modules)
    db.session.commit()


def fake_environment():
    environment = Environment(
    )
    db.session.add(environment)
    db.session.commit()


def fake_parameter():
    parameter = Parameter(
    )
    db.session.add(parameter)
    db.session.commit()


def fake_transfer():
    transfer = Transfer(
    )
    db.session.add(transfer)
    db.session.commit()


def fake_variable():
    variable = Variable(
    )
    db.session.add(variable)
    db.session.commit()
