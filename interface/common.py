from interface.Switch import switch


def trueReturn(data, msg):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }


def agreement_relation(env_verification_value, res_verification_value, v):
    """
      检验结果
      :param env_verification_value: 验证值
      :param res_verification_value: 结果返回值
      :param v: 关系
      :return:
    """
    verification = {'isTrue': False, 'msg': ''}
    for case in switch(v):
        if case('1'):
            # 等于
            if str(res_verification_value) == str(env_verification_value):
                verification['isTrue'] = True
            else:
                verification['msg'] = '返回结果 :' + str(res_verification_value) + ' != ' + ' 校验值:' + str(
                    env_verification_value)
            break
        if case('2'):
            # 不等于
            if res_verification_value != env_verification_value:
                verification['isTrue'] = True
            else:
                verification['msg'] = '返回结果 :' + str(res_verification_value) + ' == ' + ' 校验值:' + str(
                    env_verification_value)
            break
        if case('3'):
            # 包含
            if res_verification_value.find(env_verification_value) >= 0:
                verification['isTrue'] = True
            else:
                verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 不包含 ' + ' 校验值:' + str(
                    env_verification_value)
            break
        if case('4'):
            # 不包含
            if res_verification_value.find(env_verification_value) < 0:
                verification['isTrue'] = True
            else:
                verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 包含 ' + ' 校验值:' + str(
                    env_verification_value)
            break
        if case('5'):
            # 大于
            if str(res_verification_value).isdigit() == False:
                verification['isTrue'] = False
                verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 不是数字 '
            else:
                if int(res_verification_value) > int(env_verification_value):
                    verification['isTrue'] = True
                else:
                    verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 不大于 ' + ' 校验值:' + str(
                        env_verification_value)
            break
        if case('6'):
            # 大于等于
            if str(res_verification_value).isdigit() == False:
                verification['isTrue'] = False
                verification['msg'] = '返回结果 :' + res_verification_value + ' 不是数字 '
            else:
                if int(res_verification_value) >= int(env_verification_value):
                    verification['isTrue'] = True
                else:
                    verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 不大于等于 ' + ' 校验值:' + str(
                        env_verification_value)
            break
        if case('7'):
            # 小于
            if str(res_verification_value).isdigit() == False:
                verification['isTrue'] = False
                verification['msg'] = '返回结果 :' + res_verification_value + ' 不是数字 '
            else:
                if int(res_verification_value) < int(env_verification_value):
                    verification['isTrue'] = True
                else:
                    verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 不小于 ' + ' 校验值:' + str(
                        env_verification_value)
            break
        if case('8'):
            # 小于等于
            if str(res_verification_value).isdigit() == False:
                verification['isTrue'] = False
                verification['msg'] = '返回结果 :' + res_verification_value + ' 不是数字 '
            else:
                if int(res_verification_value) <= int(env_verification_value):
                    verification['isTrue'] = True
                else:
                    verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 不小于等于 ' + ' 校验值:' + str(
                        env_verification_value)
            break

        if case('9'):
            # 在列表中
            if env_verification_value in res_verification_value:
                verification['isTrue'] = True
            else:
                verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 列表中无 ' + ' 校验值:' + str(
                    env_verification_value)
            break

        if case('10'):
            # 不在列表中
            if env_verification_value not in res_verification_value:
                verification['isTrue'] = True
            else:
                verification['msg'] = '返回结果 :' + str(res_verification_value) + ' 列表中有 ' + ' 校验值:' + str(
                    env_verification_value)
            break
        if case():
            # 默认值
            print('无效判断')

    return verification
