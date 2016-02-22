#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# Last modified: 2016-02-17 23:37:23

import requests
import smtplib
from email.mime.text import MIMEText
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

data_file = "./save_file.txt"
TO_LIST = ["xxx@qq.com"]
MAIL_HOST = "smtp.163.com"
MAIL_USER = "xxx@163.com"
MAIL_PWD = "xxxxx"

def send_mail(to_list, sub, content):
    """使用smtp发邮件"""
    me = "xxxxx@163.com"
    msg = MIMEText(content, _subtype="plain", _charset="gb2312")
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(MAIL_HOST)
        server.login(MAIL_USER, MAIL_PWD)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print e
        return False


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
        "short_name": "xxxxx",
        "secret": "xxxxxx",
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
        send_mail(TO_LIST, "多说新评论", content)
    set_last_id(new_last_id)
