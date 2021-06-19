import json
import requests, asyncio, re
from telethon import events
from .. import jdbot, chat_id, _ConfigDir




# 获取京喜工厂团ID
@jdbot.on(events.NewMessage(from_users=chat_id, pattern='^/tuan'))
async def tuan(event):
    #do something
    msg = await jdbot.send_message(chat_id,"开始更新京喜工厂组团ID")
    url = 'https://cdn.jsdelivr.net/gh/gitupdate/updateTeam@master/shareCodes/jd_updateFactoryTuanId.json'
    id = ''
    i = 0
    while True:
        logrequest = requests.get(url)
        if logrequest.status_code == requests.codes.ok:
            id = logrequest.json().get('tuanActiveId')
            with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
                configs = f1.read()
                f1.close()
            await asyncio.sleep(1.5)
            if configs.find(f"export TUAN_ACTIVEID=") != -1:
                configs = re.sub(f'TUAN_ACTIVEID=(\"|\').*(\"|\')', f'TUAN_ACTIVEID="{id}"', configs)
                
            with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f2:
                f2.write(configs)
                f2.close()
            end = "替换京喜工厂团ID成功"
            break    
        else:
            await asyncio.sleep(1)
            i = i + 1
            if i > 5:
                end = "获取京喜工厂团ID失败！请重试。"
                break
    
    #await jdbot.delete_messages(chat_id, msg)
    await jdbot.send_message(chat_id,end)
