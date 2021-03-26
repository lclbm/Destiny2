import json
import os
import re
root = os.getcwd()
root = os.path.join(root, 'res', 'destiny2', 'reply')

class Untie(Exception):
    '''当没有绑定时，抛出此异常'''
    # 自定义异常类型的初始化

    # def __init__(self, value, msg):
    # 返回异常类对象的说明信息

    def __str__(self):
        return f"你似乎没有绑定自己的队伍码，请输入 绑定 【队伍码】以绑定个人信息。"



def read_json(file):
    dict_temp = {}
    try:
        with open(file, 'r', encoding='utf-8') as f:
            dict_temp = json.load(f)
            return dict_temp
    except:
        return dict_temp


def gethardlink(session):
    user_id = session.ctx['user_id']
    checkmsg = session.current_arg
    file = os.path.join(root, f'{user_id}.json')
    dict_temp = {}
    if os.path.exists(file):  # 如果文件存在的话
        dict_temp = read_json(file)
        if checkmsg == '' or checkmsg in ['术士', '猎人', '泰坦']:
            if '_self_' in dict_temp and dict_temp['_self_']['type'] == '绑定':
                if checkmsg in ['术士', '猎人', '泰坦']:
                    msg = dict_temp['_self_']['msg'] + ' ' + checkmsg
                else:
                    msg = dict_temp['_self_']['msg']
                print(msg)
                return msg
            else:
                print('没找到')
                raise Untie()
        else:
            temp = checkmsg.split()
            checkmsg = temp[0]
            if checkmsg in dict_temp and dict_temp[checkmsg]['type'] == '绑定':
                if len(temp) == 2:
                    msg = dict_temp[checkmsg]['msg'] + ' '+temp[1]
                    print(msg)
                    return msg
                else:
                    msg = dict_temp[checkmsg]['msg']
                    print(msg)
                    return msg
            else:
                return None
    else:
        return None
