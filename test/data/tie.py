import json
import os
import re
root = os.getcwd()
root = os.path.join(root, 'res', 'destiny2', 'reply')


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
                raise Exception('请输入玩家队伍码/用户名')
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
