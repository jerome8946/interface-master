# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email import encoders


import smtplib

from flask import current_app


def send_mail_with_file(filepath, filename, subject,to_addr):
    """
    发送一个带有附件（测试报告）的邮件，邮件的配置项来自sysconfig
    :param filepath: 报告文件的路径
    :param filename: 报告文件的名称
    :param subject: 邮件标题
    :return: None
    """
    # 邮件对象:
    msg = MIMEMultipart()
    msg['From'] = u"接口测试"
    msg['To'] = "you"
    msg['Subject'] = subject

    # 邮件正文是MIMEText:
    msg.attach(MIMEText(u'请查收自动化测试结果，见附件', 'plain', 'utf-8'))

    part = MIMEApplication(open(filepath, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)
    smtp_server=current_app.config['MAIL_SERVER']
    from_addr=current_app.config['MAIL_USERNAME']
    password=current_app.config['MAIL_PASSWORD']
    port=current_app.config['MAIL_PORT']
    to_addr= to_addr.split(',')
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string().encode(encoding='utf-8'))
    server.quit()
