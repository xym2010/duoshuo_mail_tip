#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# Last modified: 2016-02-17 23:37:23

import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

data_file = "./save_file.txt"

def send_message(content):
    """使用mailgun发送邮件"""
    return requests.post(
        "https://api.mailgun.net/v3/sandboxbabf1dca6cb14b46909cea514ac9c90a.mailgun.org/messages",
        auth=("api", "xxxxx"),
        data={
            "from": "xym-vps <postmaster@sandboxbabf1dca6cb14b46909cea514ac9c90a.mailgun.org>",
            "to": "xym <xxxx@qq.com>",
            "subject": "多说评论提醒",
            "text": content
        })


def get_last_id():
    with open(data_file, "r") as f:
        for line in f:
            return int(line)
        return 0


def set_last_id(last_id):
    with open(data_file, "w") as f:
        f.write(str(last_id))


if __name__ == "__main__":
    url = "http://api.duoshuo.com/log/list.json"
    params = {
        "short_name": "xxxx",
        "secret": "xxxx",
        "order": "desc"
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()
    news = []
    last_id = get_last_id()
    new_last_id = last_id
    if 'response' in data:
        log_list = data['response']
        for item in log_list:
            if 'log_id' in item and int(item['log_id']) <= last_id:
                break
            new_last_id = max(new_last_id, int(item['log_id']))
            if 'action' in item and item['action'] == 'create':
                meta = item['meta']
                news.append("[%s] %s 回复了你的《%s》：%s" % (
                    meta['created_at'],
                    meta['author_name'],
                    meta['thread_key'],
                    meta['message'],
                ))

    if news:
        content = '\n\n'.join(news)
        send_message(content)
    set_last_id(new_last_id)
