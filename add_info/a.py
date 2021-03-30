import re
import os
import json
import requests


root = os.getcwd()
user_root = os.path.join(root, 'res', 'destiny2', 'reply', 'user')
group_root = os.path.join(root, 'res', 'destiny2', 'reply', 'group')



def read_json(file):
    dict_temp = {}
    try:
        with open(file, 'r', encoding='utf-8') as f:
            dict_temp = json.load(f)
            return dict_temp
    except:
        return dict_temp


def write_json(dict_temp, path):
    with open(path, 'w', encoding='utf-8') as f:
        # 设置不转换成ascii  json字符串首缩进
        f.write(json.dumps(dict_temp, ensure_ascii=False, indent=2))


def download_img(imgurl, name):
    rsp = requests.get(imgurl)
    if rsp.status_code == 200:
        content = rsp.content
        # 注意下面open里面的mode是"wb+", 因为content的类型是bytes
        file_path = os.path.join(root, f'{name}.gif')
        with open(file_path, "wb+") as f:
            f.write(content)
            return f'[CQ:image,file=file:///{file_path}]'
    return None


def add_josn(msg, mode):
    if mode == 0:  # 管理员 All.json
        if msg['user_id'] != 614867321:
            return 0
        raw_message = msg['raw_message']
        raw_message = raw_message.replace('&#91;', '[')
        raw_message = raw_message.replace('&#93;', ']')
        message = msg['message']
        # temp = raw_message.split()
        # raw_message = ''
        # for i in temp:
        #     raw_message += i
        res = re.match(r'AddAll.*[\(|（|【](.+)】.*【(.+)】.*', raw_message)
        if not res:
            return 0
        file = os.path.join(root, 'All.json')
        dict_temp = {}
        if os.path.exists(file):  # 如果文件存在的话
            dict_temp = read_json(file)
        question = res.group(1)
        # [CQ:image,file=f46784e63445c8b7b62e06bbca04d608.image]
        answer = res.group(2)
        print(f'\n\n{question}\n\n{answer}\n\n')
        answer_res = re.match(r'.*\[CQ:image,file=(.+\.image)\].*', answer)
        # 返回的是f46784e63445c8b7b62e06bbca04d608.image
        if answer_res:  # 如果存在图片
            file_name = answer_res.group(1)
            print(f'\n\n{file_name}\n\n')
            for i in message:
                if i['type'] == 'image' and i['data']['file'] == file_name:
                    cqimg_file = download_img(
                        i['data']['url'], file_name)
                    if not cqimg_file:
                        return None
                    break
            answer = answer.replace(
                f'[CQ:image,file={file_name}]', cqimg_file)  # .img替换成了file:///
        dict_temp[question] = {'type': '自定义', 'msg': answer}
        write_json(dict_temp, file)

    if mode == 1:  # 用户绑定 614867321.json
        raw_message = msg['raw_message']
        user_id = msg['user_id']
        print(raw_message)
        res = re.match(r'绑定 +(【.*】)? *【(7656\d{13})】.*', raw_message)
        if not res:
            return None
        name1 = res.group(1)
        num = res.group(2)
        print(res.groups())
        file = os.path.join(root, f'{user_id}.json')
        dict_temp = {}
        if os.path.exists(file):  # 如果文件存在的话
            dict_temp = read_json(file)
        if not name1:
            name1 = '_self_'
        else:
            name1 = name1.replace('【', '')
            name1 = name1.replace('】', '')
        dict_temp[name1] = {'type': '绑定', 'msg': num}
        write_json(dict_temp, file)

    if mode == 2:  # 用户自定义回复 614867321.json
        raw_message = msg['raw_message']
        raw_message = raw_message.replace('&#91;', '[')
        raw_message = raw_message.replace('&#93;', ']')
        message = msg['message']
        user_id = msg['user_id']
        print(raw_message)
        # temp = raw_message.split()
        # raw_message = ''
        # for i in temp:
        #     raw_message += i
        res = re.match(r'添加.*【(.+)】.*【(.+)(】?)', raw_message)
        if not res:
            return 0
        print(res.groups())
        file = os.path.join(root, f'{user_id}.json')
        dict_temp = {}
        if os.path.exists(file):  # 如果文件存在的话
            dict_temp = read_json(file)
        question = res.group(1)
        # [CQ:image,file=f46784e63445c8b7b62e06bbca04d608.image]
        answer = res.group(2)
        if '】' in answer:
            answer = answer.replace('】','')
        answer_res = re.match(r'.*\[CQ:image,file=(.+\.image)\].*', answer)

        # 返回的是f46784e63445c8b7b62e06bbca04d608.image
        if answer_res:  # 如果存在图片
            file_name = answer_res.group(1)
            for i in message:
                if i['type'] == 'image' and i['data']['file'] == file_name:
                    cqimg_file = download_img(
                        i['data']['url'], file_name)
                    if not cqimg_file:
                        return None
                    break
            answer = answer.replace(
                f'[CQ:image,file={file_name}]', cqimg_file)  # .img替换成了file:///
        dict_temp[question] = {'type': '自定义', 'msg': answer}
        write_json(dict_temp, file)
    return 1

    if mode == 3:
        pass



def get_msg(msg):
    user_id = msg['user_id']
    checkmsg = msg['raw_message']
    file_all = os.path.join(root, 'All.json')
    file_user = os.path.join(root, f'{user_id}.json')
    dict_temp = {}
    if os.path.exists(file_all):  # 如果文件存在的话
        dict_temp = read_json(file_all)
        if checkmsg in dict_temp and dict_temp[checkmsg]['type'] == '自定义':
            print(dict_temp[checkmsg]['msg'])
            return dict_temp[checkmsg]['msg']
    if os.path.exists(file_user):  # 如果文件存在的话
        dict_temp = read_json(file_user)
        if checkmsg in dict_temp and dict_temp[checkmsg]['type'] == '自定义':
            return dict_temp[checkmsg]['msg']
    return None


def lookup(msg):
    user_id = msg['user_id']
    checkmsg = msg['raw_message']
    file_all = os.path.join(root, 'All.json')
    dict_temp = {}
    if '绑定查询 All' in checkmsg:
        if os.path.exists(file_all):  # 如果文件存在的话
            dict_temp = read_json(file_all)
            msg = '全局的自定义问答和绑定数据如下：\n'
            for i in dict_temp:
                if 'CQ:image' in i:
                    msg += '[图片]|'
                else:
                    msg += i + '|'
            print(msg)
            return msg
        return '全局没有数据，请联系小日向作者'
    file_user = os.path.join(root, f'{user_id}.json')
    if os.path.exists(file_user):  # 如果文件存在的话
        dict_temp = read_json(file_user)
        msg = '你的自定义问答和绑定数据如下：\n'
        for i in dict_temp:
            if dict_temp[i]['type'] == '绑定':
                name = i
                if 'CQ:image' in i:
                    name = '[图片]'
                id = dict_temp[i]['msg']
                msg += f'{name}:{id}|'
            else:
                if 'CQ:image' in i:
                    msg += '[图片]|'
                else:
                    msg += i + '|'
        msg += '\n输入绑定查询 All以查看全局问答'
        print(msg)
        return msg
    return '你还没有数据，请尝试添加问答和绑定'


def delimg(msg):
    res = re.match(r'.*file:///(.*gif)', msg)
    if res:
        path = res.group(1)
        if os.path.exists(path):
            os.remove(path)


def del_tie_user(msg):
    user_id = msg['user_id']
    checkmsg = msg['raw_message']
    checkmsg = checkmsg.replace('&#91;', '[')
    checkmsg = checkmsg.replace('&#93;', ']')
    if '绑定删除 All' in checkmsg and (user_id == 614867321):
        res = re.match(r'绑定删除 All.*【(.+)】.*', checkmsg)
        if not res:
            return '指令错误，输入绑定帮助以查看帮助'
        checkmsg = res.group(1)
        file_all = os.path.join(root, 'All.json')
        if os.path.exists(file_all):  # 如果文件存在的话
            dict_temp = read_json(file_all)
            if checkmsg in dict_temp:
                delimg(dict_temp[checkmsg]['msg'])
                del dict_temp[checkmsg]
                write_json(dict_temp, file_all)
                msg = f'{checkmsg} 全局删除成功'
                return msg
            else:
                return '没有找到该绑定数据，输入绑定帮助以查看帮助'
        return '全局绑定数据缺失'

    res = re.match(r'绑定删除.*【(.+)】.*', checkmsg)
    if not res:
        return '指令错误，输入绑定帮助以查看帮助'
    checkmsg = res.group(1)
    file_user = os.path.join(root, f'{user_id}.json')
    dict_temp = {}
    if os.path.exists(file_user):  # 如果文件存在的话
        dict_temp = read_json(file_user)
        if checkmsg in dict_temp:
            delimg(dict_temp[checkmsg]['msg'])
            del dict_temp[checkmsg]
            write_json(dict_temp, file_user)
            msg = f'{checkmsg} 删除成功'
            return msg
        else:
            return '没有找到该绑定数据，输入绑定帮助以查看帮助'

    return '你还没有数据，请尝试添加问答和绑定'
