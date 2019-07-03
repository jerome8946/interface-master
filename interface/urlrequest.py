# -*- coding: utf-8 -*-

'''
请求http
'''
import json
import requests
from requests import exceptions

Interface_Time_Out = 5000  # 超时时间


def get(url, params, headers):  # get消息
    try:
        r = requests.get(url, headers=headers, params=params, timeout=Interface_Time_Out)
        r.encoding = 'UTF-8'
        spend = r.elapsed.total_seconds()
        json_response = json.loads(r.text)
        status_code = r.status_code
        return json_response, spend, status_code
    except exceptions.Timeout:
        print("get请求出错,请求超时 \r\n 请求地址: %s \r\n 请求参数: %s\r\n 请求headers:  %s" % (url, params, headers))
        json_response = 'get请求出错,请求超时'
        spend = 0
        status_code = 0
        return json_response, spend, status_code
    except exceptions.InvalidURL:
        print("get请求出错,非法url \r\n 请求地址: %s \r\n 请求参数: %s\r\n 请求headers:  %s" % (url, params, headers))
        json_response = 'get请求出错,非法url'
        spend = 0
        status_code = 0
        return json_response, spend, status_code
    except exceptions.HTTPError:
        print("get请求出错,http请求错误 \r\n 请求地址: %s \r\n 请求参数: %s\r\n 请求headers:  %s" % (url, params, headers))
        json_response = 'get请求出错,http请求错误'
        spend = 0
        status_code = 0
        return json_response, spend, status_code
    except Exception as e:
        print("get请求出错,错误原因 %s \r\n 请求地址: %s \r\n 请求参数: %s\r\n 请求headers:  %s" % (e, url, params, headers))
        json_response = 'get请求出错,错误原因 错误原因：' + e.doc
        spend = 0
        status_code = 0
        return json_response, spend, status_code


def post(url, params, headers):
    """
    post消息
    :param url:
    :param params:
    :param headers:
    :return:  json_response json内容   spend响应时间
    """
    # data = json.dumps(params)
    try:
        if isinstance(headers, str):
            headers = headers.replace("\\", "")
            headers = json.loads(headers)
        r = requests.post(url, data=params, headers=headers, timeout=Interface_Time_Out)
        json_response = json.loads(r.text)
        spend = r.elapsed.total_seconds()
        status_code = r.status_code
        return json_response, spend, status_code
    except exceptions.Timeout:
        print("post请求出错,请求超时 \r\n 请求地址: %s \r\n 请求参数: %s\r\n 请求headers:  %s" % (url, params, headers))
        body = 'post请求出错,请求超时'
        spend = 0
        status_code = 0
        return body, spend, status_code
    except exceptions.InvalidURL:
        print("post请求出错,非法url \r\n 请求地址: %s \r\n 请求参数: %s\r\n 请求headers:  %s" % (url, params, headers))
        body = 'post请求出错,非法url'
        spend = 0
        status_code = 0
        return body, spend, status_code
    except exceptions.HTTPError:
        print("post请求出错,http请求错误 \r\n 请求地址: %s \r\n 请求参数: %s\r\n 请求headers:  %s" % (url, params, headers))
        body = 'post请求出错,http请求错误'
        spend = 0
        status_code = 0
        return body, spend, status_code
    except Exception as e:
        print("post请求出错,错误原因 %s \r\n 请求地址: %s \r\n 请求参数: %s\r\n 请求headers:  %s" % (e, url, params, headers))
        try:
            json_response = 'post请求出错,错误原因 错误原因：' + e.doc
        except Exception as s:
            json_response = 'post请求出错,错误原因 错误原因：' + str(e)

        spend = 0
        status_code = 0
        return json_response, spend, status_code


def delfile(url, params, headers):  # 删除的请求
    try:
        rdel_word = requests.delete(url, data=params, headers=headers, timeout=Interface_Time_Out)
        json_response = json.loads(rdel_word.text)
        spend = rdel_word.elapsed.total_seconds()
        status_code = rdel_word.status_code
        return json_response, spend, status_code
    except exceptions.Timeout:
        return {'delete请求出错': "请求超时"}
    except exceptions.InvalidURL:
        return {'delete请求出错': "非法url"}
    except exceptions.HTTPError:
        return {'delete请求出错': "http请求错误"}
    except Exception as e:
        return {'delete请求出错': "错误原因:%s" % e}


def putfile(url, params, headers):  # put请求
    try:
        rdata = json.dumps(params)
        me = requests.put(url, rdata, headers=headers, timeout=Interface_Time_Out)
        json_response = json.loads(me.text)
        spend = me.elapsed.total_seconds()
        status_code = me.status_code
        return json_response, spend, status_code
    except exceptions.Timeout:
        return {'put请求出错': "请求超时"}
    except exceptions.InvalidURL:
        return {'put请求出错': "非法url"}
    except exceptions.HTTPError:
        return {'put请求出错': "http请求错误"}
    except Exception as e:
        return {'put请求出错': "错误原因:%s" % e}


def agreement(agreement, url, headers, params):
    """
    请求
    :param agreement:   请求协议
    :param url:   请求地址
    :param headers: 请求头信息 {}
    :param params:  参数 {}
    :return:
    """

    switch = {
        "0": "GET",
        "1": "POST",
        "2": "PUT",
        "3": "DELETE"
    }

    try:
        agreement = switch[agreement]
    except KeyError as e:
        print("请求协议获取失败！")
        pass

    if agreement == 'POST' or agreement == 'post':
        response, spend, status_code = post(url=url, headers=headers, params=params)
    elif agreement == 'GET' or agreement == 'get':
        response, spend, status_code = get(url=url, headers=headers, params=params)
    elif agreement == 'PUT' or agreement == 'put':
        response, spend, status_code = putfile(url=url, params=params, headers=headers)
    elif agreement == 'DELETE' or agreement == 'delete':
        response, spend, status_code = delfile(url=url, params=params, headers=headers)
    return response, spend, status_code


if __name__ == '__main__':
    url = 'http://chenliang.xmjike.com/login'
    textmod = {}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': 'admin',
        'password': '1111'
    }

    url = "http://127.0.0.1:7777/e"
    headers = '{"Content-Type":"application/json"}'
    # data = {"c": '23'}

    response, spend, status_code = get(url=url, headers=json.loads(headers),params='')
    print(status_code)
