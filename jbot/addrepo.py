#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-17
# @Version  : v 1.0
# @Updata   :
# @Future   :
import json

from .. import chat_id, jdbot, logger, TOKEN, _JdbotDir
from ..bot.utils import press_event, backfile, _DiyDir, V4, QL, cmd, _ConfigFile, split_list, row, _Auth
from telethon import events, Button
from asyncio import exceptions
import requests, os, asyncio, re


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://github\.com/\S+git$'))
async def myaddrepo(event):
    try:
        SENDER = event.sender_id
        url = event.raw_text
        short_url, git_name = url.split('/')[-1].replace(".git", ""), url.split("/")[-2]
        btns_yn = [Button.inline("是", data="yes"), Button.inline("否", data="no")]
        if V4:
            tips_1 = [
                f'正在设置 OwnRepoBranch（分支） 的值\n该值为你想使用脚本在[仓库]({url})的哪个分支',
                '正在设置 OwnRepoPath（路径） 的值\n该值为你要使用的脚本在分支的哪个路径'
            ]
            tips_2 = [
                f'回复 main 代表使用 [{short_url}]({url}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n',
                f'回复 scripts/jd normal 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 scripts/jd 和 normal文件夹下\n回复 root cron 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 根目录 和 cron 文件夹下\n具体目录路径以你所发仓库实际为准\n'
            ]
            tips_3 = [
                [
                    Button.inline('"默认" 分支', data='root'),
                    Button.inline('"main" 分支', data='main'),
                    Button.inline('"master" 分支', data='master'),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline('仓库根目录', data='root'),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ]
            ]
        else:
            tips_1 = [
                f'正在设置 branch（分支） 的值\n该值为你想使用脚本在[仓库]({url})的哪个分支',
                f'正在设置 path（路径） 的值\n该值为你要使用的脚本在分支的哪个路径\n或你要使用根目录下哪些名字开头的脚本（可用空格或|隔开）',
                f'正在设置 blacklist（黑名单） 的值\n该值为你不需要使用以哪些名字开头的脚本（可用空格或|隔开）',
                f'正在设置 dependence（依赖文件） 的值\n该值为你想使用的依赖文件名称',
                f'正在设置定时拉取仓库的 cron 表达式，可默认每日 0 点'
            ]
            tips_2 = [
                f'回复 main 代表使用 [{short_url}]({url}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n',
                f'回复 scripts normal 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 scripts 和 normal文件夹下\n具体目录路径以你所发仓库实际为准\n',
                f'回复 jd_ jx_ 代表你不想使用开头为 jd_ 和 jx_ 的脚本\n具体文件名以你所发仓库实际、以你个人所需为准\n',
                f'回复你所需要安装依赖的文件全称\n具体文件名以你所发仓库实际、以你个人所需为准\n',
                f"回复你所需设置的 cron 表达式"
            ]
            tips_3 = [
                [
                    Button.inline('"默认" 分支', data='root'),
                    Button.inline('"main" 分支', data='main'),
                    Button.inline('"master" 分支', data='master'),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline('仓库根目录', data='root'),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline("不设置", data="root"),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline("不设置", data="root"),
                     Button.inline('手动输入', data='input'),
                     Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline("默认每天0点", data="root"),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ]
            ]
        replies = []
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            for tip_1 in tips_1:
                i = tips_1.index(tip_1)
                msg = await conv.send_message(tip_1, buttons=split_list(tips_3[i], row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'input':
                    await jdbot.delete_messages(chat_id, msg)
                    msg = await conv.send_message(tips_2[i])
                    reply = await conv.get_response()
                    res = reply.raw_text
                replies.append(res)
                await jdbot.delete_messages(chat_id, msg)
            conv.cancel()
        if V4:
            nums = []
            with open(_ConfigFile, 'r', encoding='utf-8') as f1:
                configs = f1.readlines()
            for config in configs:
                if config.find('启用其他开发者的仓库方式一') != -1:
                    start_line = configs.index(config)
                elif config.find('OwnRepoUrl1=""') != -1 and config.find("## ") == -1:
                    nums = [1]
                    break
                elif config.find('OwnRepoUrl2=""') != -1 and config.find("## ") == -1:
                    nums = [2]
                    break
                elif config.find('OwnRepoUrl') != -1 and config.find("## ") == -1:
                    num = int(re.findall(r'(?<=OwnRepoUrl)[\d]+(?==")', config)[0])
                    nums.append(num)
                elif config.find('启用其他开发者的仓库方式二') != -1:
                    end_line = configs.index(config)
                    break
            nums.sort()
            OwnRepoUrl = f'OwnRepoUrl{nums[-1] + 1}="{url}"\n'
            OwnRepoBranch = f'OwnRepoBranch{nums[-1] + 1}="{replies[0].replace("root", "")}"\n'
            Path = replies[1].replace("root", "''")
            if Path == "''":
                OwnRepoPath = f'OwnRepoPath{nums[-1] + 1}=""\n'
            else:
                OwnRepoPath = f'OwnRepoPath{nums[-1] + 1}="{Path}"\n'
            for config in configs[start_line:end_line]:
                if config.find(f'OwnRepoUrl{nums[-1]}') != -1 and config.find("## ") == -1:
                    configs.insert(configs.index(config) + 1, OwnRepoUrl)
                elif config.find(f'OwnRepoBranch{nums[-1]}') != -1 and config.find("## ") == -1:
                    configs.insert(configs.index(config) + 1, OwnRepoBranch)
                elif config.find(f'OwnRepoPath{nums[-1]}') != -1 and config.find("## ") == -1:
                    configs.insert(configs.index(config) + 1, OwnRepoPath)
            with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                f2.write(''.join(configs))
            await jdbot.send_message(chat_id, "现在开始拉取仓库，稍后请自行查看结果")
            os.system("jup own")
        else:
            branch = replies[0].replace("root", "")
            path = replies[1].replace(" ", "|").replace("root", "")
            blacklist = replies[2].replace(" ", "|").replace("root", "")
            dependence = replies[3].replace("root", "")
            cron = replies[4].replace("root", "0 0 * * *")
            cmdtext = f'ql repo {url} "{path}" "{blacklist}" "{dependence}" "{branch}"'
            res = myqladdrepo2(git_name, cmdtext, cron)
            await jdbot.send_message(chat_id, f"现在开始拉取仓库，稍后请自行查看结果")
            await cmd(cmdtext)
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^ql repo'))
async def myqladdrepo(event):
    try:
        if QL:
            SENDER = event.sender_id
            message = event.message.text
            repo = message.replace("ql repo", "")
            if len(repo) <= 1:
                await jdbot.send_message(chat_id, "没有设置仓库链接")
                return
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                msg = await conv.send_message("请设置任务名称")
                reply = await conv.get_response()
                taskname = reply.raw_text
                await jdbot.delete_messages(chat_id, msg)
                msg = await conv.send_message("请设置 cron 表达式")
                reply = await conv.get_response()
                cron = reply.raw_text
                await jdbot.delete_messages(chat_id, msg)
            myqladdrepo2(taskname, message, cron)
            await jdbot.send_message(chat_id, "开始拉取仓库，稍后请自行查看结果")
            await cmd(message)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


def myqladdrepo2(name, command, schedule):
    with open(_Auth, 'r', encoding='utf-8') as f:
        Auto = json.load(f)
    url = 'http://127.0.0.1:5600/api/crons'
    headers = {
        "Authorization": f"Bearer {Auto['token']}"
    }
    body = {
        'name': name,
        'command': command,
        'schedule': schedule
    }
    res = requests.post(url, data=body, headers=headers).json
    return res


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/repo$'))
async def myqladdrepo(event):
    try:
        SENDER = event.sender_id
        if V4:
            btns = [
                Button.inline("启动", data="start"),
                Button.inline("停止", data="stop"),
                Button.inline("删除", data="delete"),
                Button.inline("取消会话", data="cancel")
            ]
        else:
            btns = [
                Button.inline("启用", data="enable"),
                Button.inline("禁用", data="disable"),
                Button.inline("运行", data="run"),
                # Button.inline("修改", data="edit"),
                Button.inline("删除", data="del"),
                Button.inline("取消会话", data="cancel")
            ]
        if V4:
            with open(_ConfigFile, 'r', encoding='utf-8') as f:
                configs = f.readlines()
            r_names, r_urls, r_namesline, r_branchs, r_branchsline, r_paths, r_pathsline, r_status, r_nums, btns_1 = [], [], [], [], [], [], [], [], [], []
            for config in configs:
                if config.find("OwnRepoUrl") != -1 and config.find("## ") == -1:
                    url = config.split("=")[-1].replace('"', "")
                    r_urls.append(url)
                    reponum = re.findall(r"\d", config.split("=")[0])[0]
                    r_nums.append(reponum)
                    r_names.append(url.split("/")[-2])
                    r_namesline.append(configs.index(config))
                    if config.find("#") != -1:
                        status = "禁用"
                    else:
                        status = "启用"
                    r_status.append(status)
                elif config.find("OwnRepoBranch") != -1 and config.find("## ") == -1:
                    branch = config.split("=")[-1].replace('"', "")
                    if branch == '':
                        branch = "None"
                    r_branchs.append(branch)
                    r_branchsline.append(configs.index(config))
                elif config.find("OwnRepoPath") != -1 and config.find("## ") == -1:
                    path = config.split("=")[-1].replace('"', "")
                    if path == '':
                        path = "None"
                    r_paths.append(path)
                    r_pathsline.append(configs.index(config))
                elif config.find("启用其他开发者的仓库方式二") != -1:
                    break
            for r_name in r_names:
                btns_1.append(Button.inline(r_name, data=r_name))
            btns_1.append(Button.inline("更新全部仓库", data="jup"))
            btns_1.append(Button.inline("取消会话", data="cancel"))
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                msg = await conv.send_message("这是你目前添加的仓库", buttons=split_list(btns_1, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'jup':
                    msg = await jdbot.edit_message(msg, '准备拉取全部仓库')
                    os.system(res)
                    conv.cancel()
                    return
                i = r_names.index(res)
                name, url, branch, path, status, num = r_names[i], r_urls[i], r_branchs[i], r_paths[i], r_status[i], r_nums[i]
                nameline, branchline, pathline = r_namesline[i], r_branchsline[i], r_pathsline[i]
                data = f'仓库名：{name}\n仓库链接：{url}仓库分支：{branch}文件路径：{path}状态：{status}\n'
                msg = await jdbot.edit_message(msg, f'{data}请做出你的选择', buttons=split_list(btns, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'start':
                    await jdbot.edit_message(msg, "启动仓库")
                    configs[nameline] = configs[nameline].replace("# ", "")
                    configs[branchline] = configs[branchline].replace("# ", "")
                    configs[pathline] = configs[pathline].replace("# ", "")
                    configs = ''.join(configs)
                elif res == 'stop':
                    await jdbot.edit_message(msg, "停止仓库")
                    configs[nameline] = f"# {configs[nameline]}"
                    configs[branchline] = f"# {configs[branchline]}"
                    configs[pathline] = f"# {configs[pathline]}"
                    configs = ''.join(configs)
                elif res == 'delete':
                    await jdbot.edit_message(msg, "删除仓库")
                    with open(_ConfigFile, 'r', encoding='utf-8') as f:
                        configs = f.read()
                    configs = re.sub(f"OwnRepoUrl{num}=.*", "", configs)
                    configs = re.sub(f"OwnRepoBranch{num}=.*", "", configs)
                    configs = re.sub(f"OwnRepoPath{num}=.*", "", configs)
                with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                    f2.write(configs)
        else:
            crontabfpaht = "/ql/db/crontab.db"
            with open(crontabfpaht, 'r', encoding='utf-8') as f:
                crontabs = f.readlines()
            datas, names, btns_1 = [], [], []
            for crontab in crontabs:
                if crontab.find("ql repo ") != -1 and crontab.find('"saved":true,"') != -1:
                    data = json.loads(crontab)
                    datas.append(crontab)
                    names.append(data['name'])
            names = list(set(names))
            for name in names:
                btns_1.append(Button.inline(name, data=name))
            btns_1.append(Button.inline("取消会话", data="cancel"))
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                msg = await conv.send_message("这是你目前添加的仓库", buttons=split_list(btns_1, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                i = names.index(res)
                data = json.loads(datas[i])
                name = data['name']
                command = data['command'].replace("ql repo ", "")
                schedule = data['schedule']
                isDisabled = data['isDisabled']
                _id = data['_id']
                if isDisabled == 0:
                    status = "启用"
                else:
                    status = "禁用"
                info = f"任务名：{name}\n命令：{command}\n定时：{schedule}\n状态：{status}\n"
                msg = await jdbot.edit_message(msg, f"{info}请做出你的选择", buttons=split_list(btns, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                with open(_Auth, 'r', encoding='utf-8') as f:
                    Auto = json.load(f)
                url = 'http://127.0.0.1:5600/api/crons'
                headers = {"Authorization": f"Bearer {Auto['token']}"}
                body = [_id]
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'run':
                    msg = await jdbot.edit_message(msg, "正在拉取仓库")
                    requests.put(f'{url}/run', json=body, headers=headers)
                elif res == 'enable':
                    msg = await jdbot.edit_message(msg, "启用拉取仓库任务")
                    requests.put(f'{url}/enable', json=body, headers=headers)
                elif res == 'disable':
                    msg = await jdbot.edit_message(msg, "禁用拉取仓库任务")
                    requests.put(f'{url}/disable', json=body, headers=headers)
                elif res == 'del':
                    msg = await jdbot.edit_message(msg, "删除拉取仓库任务")
                    requests.delete(url, json=body, headers=headers)
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
