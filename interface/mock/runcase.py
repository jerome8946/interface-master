# # -*- coding: utf-8 -*-
# import datetime
# import json
# import os
# import uuid
#
# from dotenv import load_dotenv
#
# from interface import appInster
# from interface.EmailOperate import send_mail_with_file
# from interface.common import agreement_relation
# from interface.interprints.reportLog import deleteScheduling, getExecl
# from interface.mock.implement import run_interface
# from interface.models import UserCase, Environment, Variable, db, Report
# from interface.randomCode import getRanges, resEn, resFloat, resDate, string_toDatetime
# from interface.urlrequest import agreement
# from interface.utils import getJsonValue, getRelationship, txt_wrap_by
#
# current_path = os.path.abspath('.')
#
#
# def test_case(case_id, report_case_type, request_address, report_create_time):
#     """
#     执行case
#     :param user_case:
#     :return:
#     """
#     user_case = UserCase.query.get_or_404(case_id)
#     caseJson = {}
#     caseJson['case_name'] = user_case.case_name
#     caseJson['uc_id'] = user_case.uc_id
#     for case_env in user_case.case_env:
#         # 需要执行的接口
#         case_env_dict = {}
#         case_env_dict['case_id'] = case_env.case_id
#         case_env_dict['env_id'] = case_env.env_id
#         case_env_dict['modules_id'] = case_env.modules_id
#         case_env_dict['project_id'] = case_env.project_id
#
#         run_interface(case_env.env_id, case_id, report_case_type, request_address, report_create_time, scheduling_id='')
#
#
# def test_caseList(caseList, scheduling_id='', email_address=None):
#     """
#     执行caseList
#     :param caseList:
#     :return:
#     """
#     app = appInster.app
#     with app.app_context():
#         deleteScheduling(scheduling_id)
#         for case_id in caseList:
#             user_case = UserCase.query.get_or_404(case_id['case_id'])
#             caseJson = {}
#             caseJson['case_name'] = user_case.case_name
#             caseJson['uc_id'] = user_case.uc_id
#             for case_env in user_case.case_env:
#                 # 需要执行的接口
#                 case_env_dict = {}
#                 case_env_dict['case_id'] = case_env.case_id
#                 case_env_dict['env_id'] = case_env.env_id
#                 case_env_dict['modules_id'] = case_env.modules_id
#                 case_env_dict['project_id'] = case_env.project_id
#                 case_time = str(uuid.uuid1())
#                 report_create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#                 run_interface(case_env.env_id, case_id['case_id'], case_time, case_env.user_case.request_address,
#                               report_create_time, scheduling_id)
#         # 发送邮件
#         execlName = scheduling_id.replace('-', '')
#         getExecl(scheduling_id=scheduling_id, execlName=execlName)
#         if email_address != None and len(email_address) > 0:
#             email_address = email_address
#             startPath = os.path.join(current_path, 'logs\\' + execlName + '_interface.xlsx')
#             send_mail_with_file(filepath=startPath, filename=u"interface.xlsx", subject=u'接口自动化测试',
#                                 to_addr=email_address)
#
#
# # def run_interface(env_id, case_id, report_case_type, request_address, report_create_time, scheduling_id):
# #     """
# #     执行接口
# #     :param env_id: 接口id
# #     :return:
# #     """
# #     # 获取该接口的数据信息
# #     env = Environment.query.get_or_404(env_id)
# #
# #     for transfer in env.transfer:
# #         for variable in transfer.variable:
# #             variable = Variable.query.get_or_404(variable.var_id)
# #             variable.var_value = ""
# #             db.session.commit()
# #
# #     env = Environment.query.get_or_404(env_id)
# #
# #     envJson = {}
# #     envJson['env_name'] = env.env_name
# #     envJson['env_desc'] = env.env_desc
# #     envJson['env_transmission'] = env.env_transmission
# #     envJson['env_agreement'] = env.env_agreement
# #     envJson['env_path'] = env.env_path
# #     envJson['env_verification'] = env.env_verification
# #     envJson['project_id'] = env.project_id
# #     envJson['modules_id'] = env.modules_id
# #     envJson['env_status'] = env.env_status
# #     envJson['env_complete'] = env.env_complete
# #     envJson['env_ip'] = env.env_ip
# #     envJson['env_port'] = env.env_port
# #     envJson['env_id'] = env.env_id
# #
# #     transfer_jsonarray = []
# #     for transfer in env.transfer:
# #         transfer_dict = {}
# #         transfer_dict['tra_transfer_id'] = transfer.tra_transfer_id
# #         transfer_dict['tra_need_env_id'] = transfer.tra_need_env_id
# #         transfer_dict['tra_modulated_env_id'] = transfer.tra_modulated_env_id
# #         tra_modulated_env = Environment.query.get_or_404(transfer.tra_modulated_env_id)
# #         transfer_dict['project_id'] = tra_modulated_env.project_id
# #         transfer_dict['modules_id'] = tra_modulated_env.modules_id
# #         variable_list = []
# #         for variable in transfer.variable:
# #             variable_dict = {}
# #             variable_dict['var_id'] = variable.var_id
# #             variable_dict['transfer_id'] = variable.transfer_id
# #             variable_dict['var_name'] = variable.var_name
# #             variable_dict['var_regexp'] = variable.var_regexp
# #             variable_dict['var_value'] = variable.var_value
# #             variable_list.append(variable_dict)
# #         transfer_dict['variable'] = variable_list
# #         transfer_jsonarray.append(transfer_dict)
# #         # 调用其他接口获取参数  传入需要调用的接口id   参数名称
# #         invoking(transfer.tra_modulated_env_id, variable_list, case_id, report_case_type, request_address,
# #                  report_create_time, scheduling_id)
# #
# #     env = Environment.query.get_or_404(env_id)
# #     # 找出所有的变量和变量值
# #     var_value_list = {}
# #     for tar in env.transfer:
# #         for varObject in tar.variable:
# #             var_value_list[varObject.var_name] = varObject.var_value
# #
# #     par_data = {}
# #     for parameter in env.parameter:
# #         if parameter.par_correct != "":
# #             par_data[parameter.par_us_name] = parameter.par_correct
# #         elif parameter.par_correct == "" and parameter.par_variable == "":
# #             par_data[parameter.par_us_name] = ""
# #         else:
# #             par_data[parameter.par_us_name] = var_value_list[parameter.par_variable]
# #
# #     # envJson['env_headers'] = env.env_headers
# #     # 通过接口ID获取请求信息头
# #     headers_dict = {}
# #     # headers 变量设值
# #     for header in env.headerValue:
# #         if header.header_value.find('${') >= 0:
# #             # 获取${} 里面的值
# #             headerParm = txt_wrap_by("${", "}", header.header_value)
# #             headers_dict[header.header_name] = header.header_value.replace("${" + headerParm + "}",
# #                                                                            var_value_list[headerParm])
# #         else:
# #             headers_dict[header.header_name] = header.header_value
# #
# #     envJson['env_headers'] = headers_dict
# #
# #     # 接口请求case
# #     case_list = []
# #     # 没有调用其他接口
# #     for parameter in env.parameter:
# #         if parameter.par_correct != "":
# #             case_explain = '参数_' + parameter.par_us_name + '_value_' + parameter.par_correct + '_' + parameter.par_cn_name + '正确参数CASE'
# #             setParameter_dict(case_list, parameter, par_data, parameter.par_correct, case_explain, "1", case_id)
# #         else:
# #             if len(var_value_list) > 0:
# #                 varvluelist = var_value_list[parameter.par_variable]
# #             else:
# #                 varvluelist = " "
# #
# #             case_explain = '参数_' + parameter.par_us_name + '_value_' + varvluelist + '_' + parameter.par_cn_name + '正确参数CASE'
# #             setParameter_dict(case_list, parameter, par_data, varvluelist, case_explain, "1", case_id)
# #
# #         # 判断是否必填
# #         case_explain = ""
# #         if parameter.par_required == 1:
# #             print('必填')
# #             case_explain = "参数_" + parameter.par_us_name + "_value_" + '_' + parameter.par_cn_name + '必填项为空CASE'
# #             setParameter_dict(case_list, parameter, par_data, "", case_explain, "1", case_id)
# #         else:
# #             print('非必填')
# #             case_explain = "参数_" + parameter.par_us_name + "_value_" '_' + parameter.par_cn_name + '非必填项为空CASE'
# #             setParameter_dict(case_list, parameter, par_data, "", case_explain, "2", case_id)
# #
# #         # 获取限制范围长度
# #         par_range = parameter.par_range
# #         length_range = getRanges(par_range)
# #         if len(par_range.split('-')) > 1:
# #             start_len = int(length_range[0])
# #             end_len = int(length_range[1])
# #             float_len = int(length_range[2])
# #         # 判断类型
# #         if parameter.par_type == '0':
# #             print('参数类型字符串')
# #             # 随机生成英文字符串
# #             if len(par_range) > 0:
# #                 resStr = resEn(start_len, end_len)
# #                 case_explain = "参数_" + parameter.par_us_name + "_value_" + resStr + '_' + parameter.par_cn_name + '限制范围内英文字符CASE'
# #                 setParameter_dict(case_list, parameter, par_data, resStr, case_explain, "1", case_id)
# #
# #                 resStr = resEn(1, end_len + 5)
# #                 case_explain = "参数_" + parameter.par_us_name + "_value_" + resStr + '_' + parameter.par_cn_name + '限制范围外英文字符CASE'
# #                 setParameter_dict(case_list, parameter, par_data, resStr, case_explain, "2", case_id)
# #         elif parameter.par_type == '1':
# #             print('参数类型数字')
# #             # 限制数字输入英文
# #             resStr = resEn(1, 5)
# #             case_explain = "参数_" + parameter.par_us_name + "_value_" + resStr + '_' + parameter.par_cn_name + '参数类型数字输入英文字符CASE'
# #             setParameter_dict(case_list, parameter, par_data, resStr, case_explain, "2", case_id)
# #
# #             if len(par_range) > 0:
# #                 # 取值范围内
# #                 resStr = resFloat(start_len, end_len, float_len)
# #                 case_explain = "参数_" + parameter.par_us_name + "_value_" + str(
# #                     resStr) + '_' + parameter.par_cn_name + '参数类型数字取值范围内CASE'
# #                 setParameter_dict(case_list, parameter, par_data, str(resStr), case_explain, "1", case_id)
# #
# #                 # 小于取值范围
# #                 resStr = resFloat(start_len / 10, start_len / 2, float_len)
# #                 case_explain = "参数_" + parameter.par_us_name + "_value_" + str(
# #                     resStr) + '_' + parameter.par_cn_name + '参数类型数字小于取值范围CASE'
# #                 setParameter_dict(case_list, parameter, par_data, str(resStr), case_explain, "2", case_id)
# #
# #                 # 大于取值范围
# #                 resStr = resFloat(end_len + 1, end_len + 10, float_len)
# #                 case_explain = "参数_" + parameter.par_us_name + "_value_" + str(
# #                     resStr) + '_' + parameter.par_cn_name + '参数类型数字大于取值范围CASE'
# #                 setParameter_dict(case_list, parameter, par_data, str(resStr), case_explain, "2", case_id)
# #
# #         elif parameter.par_type == '2':
# #             print("日期格式")
# #             # 获取日期格式
# #             par_date_type = parameter.par_date_type
# #
# #             par_start_date = parameter.par_start_date
# #             par_end_date = parameter.par_end_date
# #
# #             s_year, s_month, s_day, s_hour, s_minute, s_second = string_toDatetime(par_start_date, par_date_type)
# #             e_year, e_month, e_day, e_hour, e_minute, e_second = string_toDatetime(par_end_date, par_date_type)
# #
# #             # 正确的日期case
# #             resdate = resDate(s_year, s_month, s_day, s_hour, s_minute, s_second, e_year, e_month, e_day, e_hour,
# #                               e_minute, e_second, par_date_type)
# #
# #             case_explain = "参数_" + parameter.par_us_name + "_value_" + resdate + '_' + parameter.par_cn_name + '参数类型日期取值范围内CASE'
# #             setParameter_dict(case_list, parameter, par_data, resdate, case_explain, '1', case_id)
# #
# #             # 非日期格式范围
# #             resdate = resEn(1, 5)
# #             case_explain = "参数_" + parameter.par_us_name + "_value_" + resdate + '_' + parameter.par_cn_name + '参数类型日期非日期格式CASE'
# #             setParameter_dict(case_list, parameter, par_data, resdate, case_explain, '2', case_id)
# #     if len(env.parameter) == 0:
# #         case_explain = "参数_" + '' + "_value_" + '' + "_无参数请求"
# #         setParameter_dict(case_list, '', par_data, '', case_explain, '1', case_id)
# #
# #     env_transmission = "http"
# #     if env.env_transmission != '0':
# #         env_transmission = "https"
# #     if request_address != None:
# #         request_address = request_address.strip()
# #         if request_address[-1] == '/':
# #             request_address = request_address[:-1]
# #         url = env_transmission + "://" + request_address + "/" + env.env_path
# #     else:
# #         url = env_transmission + "://" + env.env_ip + ":" + env.env_port + "/" + env.env_path
# #     for case in case_list:
# #         response, spend, status_code = agreement(agreement=env.env_agreement, url=url,
# #                                                  headers=headers_dict,
# #                                                  params=case['case_dict'])
# #         report_env_pass = 0
# #         check_str = ""
# #         case_explain = case['case_explain'].split('_')
# #         print("------------------------------------------------------------------")
# #         print("case_explain : " + case['case_explain'])
# #         print("case标题 %s " % (case_explain[4]))
# #         print("请求地址 %s " % (url))
# #         print("请求参数 %s " % (str(case['case_dict'])))
# #         print("返回http status %s " % (status_code))
# #         print("接口响应时间 %s " % (spend))
# #         print("后台返回数据信息 %s  " % (response))
# #
# #         # 判断是否执行通过
# #         if status_code == 200:
# #             # 判断校验的code是否通过
# #             env_verification = json.loads(env.env_verification)
# #             env_verification_code = env_verification['env_verification_code']  # 需要校验
# #             env_agreement_relation = env_verification['env_agreement_relation']
# #             env_verification_value = env_verification['env_verification_value']
# #             res_verification_value = getJsonValue(env_verification_code, response)
# #
# #             isTrue = agreement_relation(env_verification_value, res_verification_value, env_agreement_relation)
# #             if isTrue['isTrue']:
# #                 report_env_pass = 0
# #                 print("用例执行通过")
# #             else:
# #                 if case['case_index'] == "2":
# #                     report_env_pass = 0
# #                     print("用例执行通过")
# #                 else:
# #                     report_env_pass = 1
# #                     print("用例执行失败")
# #                     print("预计校验规则 code %s 关系: %s value: %s" % (
# #                         env_verification_code, getRelationship(env_agreement_relation), env_verification_value))
# #                     print("实际返回数据 code %s  value: %s" % (env_verification_code, res_verification_value))
# #
# #                     check_str = "\r\n" + "校验规则:" + "\r\n" + " 校验路径:" + env_verification_code + "关系:" + getRelationship(
# #                         env_agreement_relation) + " 校验值: " + str(env_verification_value) + "\r\n" + isTrue['msg']
# #         elif status_code != 0:
# #             report_env_pass = 1
# #             print("请求出错")
# #
# #         addReport(case_explain[4], url, str(case['case_dict']), status_code, spend, str(response) + check_str,
# #                   case_id,
# #                   report_env_pass, report_case_type, report_create_time, scheduling_id)
# #
# #         print("------------------------------------------------------------------")
# #
# #
# # def invoking(tra_modulated_env_id, variable_list, case_id, report_case_type, request_address, report_create_time,
# #              scheduling_id):
# #     """
# #     调用其他接口获取参数值
# #     :param tra_modulated_env_id: 被调用的接口id
# #     :return:
# #     """
# #     env = Environment.query.get_or_404(tra_modulated_env_id)
# #
# #     for transfer in env.transfer:
# #         for variable in transfer.variable:
# #             variable = Variable.query.get_or_404(variable.var_id)
# #             variable.var_value = ""
# #             db.session.commit()
# #
# #     env = Environment.query.get_or_404(tra_modulated_env_id)
# #
# #     envJson = {}
# #     envJson['env_name'] = env.env_name
# #
# #     # envJson['env_headers'] = env.env_headers
# #     headers_dict = {}
# #     for header in env.headerValue:
# #         headers_dict[header.header_name] = header.header_value
# #
# #     envJson['env_status'] = env.env_status  # 状态 是否被禁用
# #     envJson['env_complete'] = env.env_complete  # 是否开发完成 是否开发完成
# #     envJson['env_id'] = env.env_id
# #
# #     for transfer in env.transfer:
# #         # 调用其他接口获取参数
# #         transfer_dict = {}
# #         transfer_dict['tra_transfer_id'] = transfer.tra_transfer_id
# #         transfer_dict['tra_need_env_id'] = transfer.tra_need_env_id
# #         transfer_dict['tra_modulated_env_id'] = transfer.tra_modulated_env_id
# #         tra_modulated_env = Environment.query.get_or_404(transfer.tra_modulated_env_id)
# #         transfer_dict['project_id'] = tra_modulated_env.project_id
# #         transfer_dict['modules_id'] = tra_modulated_env.modules_id
# #
# #         variable_list_object = []
# #         for variable in transfer.variable:
# #             variable_dict = {}
# #             variable_dict['var_id'] = variable.var_id
# #             variable_dict['transfer_id'] = variable.transfer_id
# #             variable_dict['var_name'] = variable.var_name
# #             variable_dict['var_regexp'] = variable.var_regexp
# #             variable_dict['var_value'] = variable.var_value
# #             variable_list_object.append(variable_dict)
# #
# #         invoking(transfer.tra_modulated_env_id, variable_list_object, case_id, report_case_type, request_address,
# #                  report_create_time, scheduling_id)
# #
# #     # 获取参数
# #     parameter_dict = {}
# #     env = Environment.query.get_or_404(tra_modulated_env_id)
# #     variableObj = {}
# #     for transferObj in env.transfer:
# #         for variable in transferObj.variable:
# #             variableObj[variable.var_name] = variable.var_value
# #
# #     # headers 变量设值
# #     for header in env.headerValue:
# #         if header.header_value.find('${') == 1:
# #             # 获取${} 里面的值
# #             headerParm = txt_wrap_by("${", "}", header.header_value)
# #             headers_dict[header.header_name] = variableObj[headerParm]
# #         else:
# #             headers_dict[header.header_name] = header.header_value
# #
# #     for parameter in env.parameter:
# #         if parameter.par_correct != '' or parameter.par_correct is not None:
# #             parameter_dict[parameter.par_us_name] = parameter.par_correct
# #         else:
# #             parameter_dict[parameter.par_us_name] = variableObj[parameter.par_variable]
# #
# #     # 根据参数预设的值进行接口请求
# #     env_transmission = "http"
# #     if env.env_transmission != '0':
# #         env_transmission = "https"
# #     if request_address != None:
# #         request_address = request_address.strip()
# #         if request_address[-1] == '/':
# #             request_address = request_address[:-1]
# #         url = env_transmission + "://" + request_address + "/" + env.env_path
# #     else:
# #         url = env_transmission + "://" + env.env_ip + ":" + env.env_port + "/" + env.env_path
# #     response, spend, status_code = agreement(agreement=env.env_agreement, url=url, headers=headers_dict,
# #                                              params=parameter_dict)
# #     report_env_pass = 0
# #     check_str = ''
# #     print("------------------------------------------------------------------")
# #     print("调用接口")
# #     print("请求地址 %s " % (url))
# #     print("请求参数 %s " % (parameter_dict))
# #     print("返回http status %s " % (status_code))
# #     print("接口响应时间 %s" % (spend))
# #     print("------------------------------------------------------------------")
# #
# #     # 判断是否执行通过
# #     if status_code == 200:
# #
# #         # 判断校验的code是否通过
# #         env_verification = json.loads(env.env_verification)
# #         env_verification_code = env_verification['env_verification_code']  # 需要校验
# #         env_agreement_relation = env_verification['env_agreement_relation']
# #         env_verification_value = env_verification['env_verification_value']
# #
# #         res_verification_value = getJsonValue(env_verification_code, response)
# #
# #         if str(res_verification_value) == str(env_verification_value):
# #             print("执行通过")
# #             # 获取要取变量的值，并加入数据库中
# #             for variable in variable_list:
# #                 var_id = variable['var_id']
# #                 var_regexp = variable['var_regexp']
# #                 var_value = getJsonValue(var_regexp, response)
# #                 # 添加到数据库
# #                 variable = Variable.query.get_or_404(var_id)
# #                 # 判断返回内容是否是json
# #                 variable.var_value = var_value
# #                 db.session.commit()
# #         else:
# #             report_env_pass = 1
# #             print("预计校验规则 code %s 关系: %s value: %s" % (
# #                 env_verification_code, getRelationship(env_agreement_relation), env_verification_value))
# #             print("实际返回数据 code %s  value: %s" % (env_verification_code, res_verification_value))
# #
# #             check_str = "\r\n预计校验规则 code %s 关系: %s value: %s" % (
# #                 env_verification_code, getRelationship(env_agreement_relation),
# #                 env_verification_value) + "\r\n" + "实际返回数据 code %s  value: %s" % (
# #                             env_verification_code, res_verification_value)
# #     elif status_code != 200:
# #         report_env_pass = 1
# #         print("请求出错")
# #
# #     addReport("调用上级接口", url, str(parameter_dict), status_code, spend, str(response) + check_str, case_id,
# #               report_env_pass, report_case_type, report_create_time, scheduling_id)
#
#
# def setParameter_dict(case_list, parameter, par_data, resStr, case_str, case_index, case_id):
#     """
#     设置case集合
#     :param case_list:   case集合
#     :param parameter:  参数
#     :param resStr: 随机内容
#     :param case_str:  case说明
#     :param case_index:  正向case 1  逆向case 2
#     :return:
#     """
#     case_dict = {}
#     if len(par_data) > 0:
#         par_data_set = par_data.copy()
#         par_data_set[parameter.par_us_name] = resStr
#         case_dict['case_dict'] = par_data_set
#     else:
#         case_dict['case_dict'] = ''
#
#     case_dict['case_explain'] = case_str
#     case_dict['case_index'] = case_index
#     case_dict['case_id'] = case_id
#     case_list.append(case_dict)
#
#
# def addReport(report_title, report_url, report_env_param, report_env_status, report_env_time,
#               report_env_response, case_id, report_env_pass, report_case_type, report_create_time, scheduling_id):
#     """
#     报告添加
#     :param report_env_call:  是否是调用的接口
#     :param report_title:  case标题
#     :param report_url:  请求地址
#     :param report_env_param: 请求参数
#     :param report_env_status: 返回状态
#     :param report_env_time: 接口返回时间
#     :param report_env_response:  接口返回信息
#     :param case_id:   case  id
#     :return:
#     """
#     report = Report(report_title=report_title, report_url=report_url,
#                     report_env_param=report_env_param, report_env_status=report_env_status,
#                     report_env_time=report_env_time, report_env_response=report_env_response, uc_id=case_id,
#                     report_env_pass=report_env_pass, report_case_type=report_case_type,
#                     report_create_time=report_create_time, scheduling_id=scheduling_id)
#     db.session.add(report)
#     db.session.commit()
#
#
# if __name__ == '__main__':
#     peizhi = 'resNum.0.b'
#     body = {'msg': '请求C成功', 'msg_code': 100, 'resNum': [{"b": "11"}, {"b": '33'}]}
#     peizhi = peizhi.split(".")
#     # 为了获取b的值
#     key = ""
#     for i in range(len(peizhi)):
#         key = peizhi[i]
#     if key.isdigit():
#         key = int(key)
#     body = body[key]  # 获取到resNum的值
#     print(body)
