# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import smtplib
import time
import ConfigParser
import os
import math
from email.mime.text import MIMEText


def check(duoshuo):
    url = 'http://api.duoshuo.com/log/list.json?' \
          + 'short_name=' + duoshuo['short_name'] \
          + '&secret=' + duoshuo['secret']
    r = requests.get(url)

    resp = r.json()
    if(resp['code'] == 0):
        return len(resp['response'])
    return 0


def send_email(email, content):
    msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg['Subject'] = '多说评论通知'
    msg['From'] = email['from']
    msg['To'] = email['to']
    try:
        server = smtplib.SMTP()
        server.connect(email['host'])
        server.login(email['name'], email['password'])
        server.sendmail(email['from'], [email['to']], msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

def prepareContent(res,website):
    con = ""
    if res['action'] == 'create':
        con = unicode('***************************************************\n' + '文章：' + website + res['meta']['thread_key'] + '\n作者：' + res['meta']['author_name']+ '\n内容：' + res['meta']['message']) + '\n\n'
    return con

def run():
    print '开始运行'
    conf = ConfigParser.RawConfigParser()
    path = os.path.dirname(__file__)
    conf_file = os.path.join(path, 'conf/duoshuo.conf')
    conf.read(conf_file)

    duoshuo = {}
    for item in conf.items('duoshuo'):
        duoshuo[item[0]] = item[1]

    email = {}
    for item in conf.items('email'):
        email[item[0]] = item[1]

    others = {}
    for item in conf.items('others'):
        others[item[0]] = item[1]

    stime = int(30)

    last_count = current_count = check(duoshuo)

    content = 'http://' + duoshuo['short_name'] + '.duoshuo.com/admin/'
    content = ""
    while True:
        url = 'http://api.duoshuo.com/log/list.json?' \
              + 'short_name=' + duoshuo['short_name'] \
              + '&secret=' + duoshuo['secret']
        r = requests.get(url)

        resp = r.json()

        ##获取新的数目
        if(resp['code'] == 0):
            current_count = len(resp['response'])
        else:
            current_count = 0
        print current_count
        last_count = 45
        ##若有新内容，则把新内容遍历，并且发送详情到邮箱
        if(current_count > last_count):
            nums = current_count - last_count
            for num in range(0,nums):
                 content = content + prepareContent(resp['response'][current_count - 1 - num],duoshuo['website'])
            if content != "":
                print content
                send_email(email, content)
            last_count = current_count

        time.sleep(stime)


if __name__ == '__main__':
    run()
