# -*- coding: utf-8 -*-
import datetime
import string
import random
import time
import numpy as np


def resEn(count, length):
    """
    英文数字随机
    :param count: 几组
    :param length: 长度
    :return:
    """
    selectWord = string.ascii_letters + "0123456789"
    for x in range(count):
        re = ""
        for y in range(int(length)):
            re += random.choice(selectWord)
    return re


def resNum(count, length):
    """
    数字随机
    :param count: 几组
    :param length: 长度
    :return:
    """
    selectWord = "0123456789"
    for x in range(count):
        re = ""
        for y in range(length):
            re += random.choice(selectWord)
    return re


def resGBK2312(count, length):
    """
    中文随机
    :param count: 组
    :param length: 长度
    :return:
    """
    str = ""
    for x in range(count):
        for i in range(length):
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            val = f'{head:x}{body:x}'
            str = str + bytes.fromhex(val).decode('gb2312')
    return str


def resDate(s_year, s_month, s_day, s_hour, s_minute, s_second,e_year, e_month, e_day, e_hour, e_minute, e_second, format):
    """
    随机日期
    :param startYear: 开始日期
    :param endYear: 结束日期
    :param format "%Y-%m-%d"
    %y 两位数的年份表示（00-99）
    %Y 四位数的年份表示（000-9999）
    %m 月份（01-12）
    %d 月内中的一天（0-31）
    %H 24小时制小时数（0-23）
    %I 12小时制小时数（01-12）
    %M 分钟数（00=59）
    %S 秒（00-59）
    :return:
    """
    a1 = (s_year, s_month, s_day, s_hour, s_minute, s_second, 0, 0, 0)  # 设置开始日期时间元组（endYear-01-01 00：00：00）
    a2 = (e_year, e_month, e_day, e_hour, e_minute, e_second, 0, 0, 0)  # 设置结束日期时间元组（endYear-12-31 23：59：59）
    start = time.mktime(a1)  # 生成开始时间戳
    end = time.mktime(a2)  # 生成结束时间戳
    t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
    date_touple = time.localtime(t)  # 将时间戳生成时间元组
    date = time.strftime(format, date_touple)  # 将时间元组转成格式化字符串（xxxx-xx-xx）
    print(date)
    return date


def resFloat(s, e, j):
    """
    生成任意范围任意精度的随机数
    :param s: 开始精度
    :param e: 结束精度
    :param j : 精度
    :return:
    """
    random = np.random.RandomState(0)  # RandomState生成随机数种子
    a = random.uniform(int(s), int(e))  # 随机数范围
    x = round(a, int(j))  # 随机数精度要求
    if j == 0:
        x = str(x).replace('.0', '')
    print(x)
    return x


def getRanges(rangeNum):
    """
    获取数值范围
    :param range: 范围
    :return:
    """
    rangeNums = rangeNum.split('-')

    return rangeNums


def string_toDatetime(date, format):
    """
    获取日期的年月日时分秒
    :param date:
    :param format:
    :return:
    """
    # date = datetime.datetime.strptime(date, format)
    date = time.strptime(date, format)
    year = date.tm_year
    month = date.tm_mon
    day = date.tm_mday
    hour = date.tm_hour
    minute = date.tm_min
    second = date.tm_sec
    return year, month, day, hour, minute, second


if __name__ == '__main__':

    a=resFloat(10, 20, 1)
    print(a)
    # resDate(1995, 1, 10, 2003, 2, 28, '%Y-%m-%d')
