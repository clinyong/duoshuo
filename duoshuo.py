# coding: utf-8

import requests
import smtplib
import time
import ConfigParser
import os
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


def run():
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

    stime = int(others['sleep_time'])

    last_count = current_count = check(duoshuo)

    content = 'http://' + duoshuo['short_name'] + '.duoshuo.com/admin/'

    while True:
        current_count = check(duoshuo)
        if(current_count > last_count):
            send_email(email, content)
            last_count = current_count

        time.sleep(stime)


if __name__ == '__main__':
    run()
