# -*- coding: utf8 -*-

#######  执行
'''
   apt-get install python3-pip
   pip3 install requests termcolor bs4
'''
########

import sys, requests, re, random
from datetime import *
# from bs4 import BeautifulSoup
from http.cookiejar import LWPCookieJar
from multiprocessing.dummy import Pool as ThreadPool
from termcolor import *

username = 'brady_xiong'
password = 'BRADYpassw0rd'

now = str(datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))).split('.')[0]
cookies = LWPCookieJar(filename='cookies.txt')


def login(user, password):
    # data['username'] = sys.argv[1]
    # data['password'] = sys.argv[2]

    login_url = 'http://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'

    data = {
        'fastloginfield': 'username',
        'handlekey': 'ls',
        'password': password,
        'quickforward': 'yes',
        'username': user
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)'
    }

    # 保存登录信息cookies
    session = requests.session()
    session.cookies = cookies
    response = session.post(login_url, data=data, headers=headers)

    # 判断登录成功
    if response.ok and re.findall(r"www.hostloc.com", response.text):
        cookies.save(ignore_discard=True)  # 保存登录信息cookies
        # cookies.load(ignore_discard=True)
        print(colored(now + '登录成功', 'green'))
        return session
    else:
        print(colored(now + '登录失败，系统自动退出', 'red'))
        exit()


def score(sess):
    bscore = re.findall(r'积分: ([0-9]+)', sess.get('http://www.hostloc.com/forum.php').content.decode('utf-8'))[0]
    print('Hostloc签到前积分: ', bscore)

    pool = ThreadPool(10)  # 10个线程

    urls = ['http://www.hostloc.com/space-uid-{}.html'.format(random.randint(10000, 20000)) for i in
            range(20)]

    results = pool.map(lambda x: sess.get(x), urls)  # urls是任务列表 list，第一个参数是线程函数
    # close the pool
    pool.close()
    pool.join()

    ascore = re.findall('积分: ([0-9]+)', sess.get('http://www.hostloc.com/forum.php').content.decode('utf-8'))[0]
    print('Hostloc签到后积分: ', bscore)

    print(colored('签到成功！', 'green')) if (int(ascore) - int(bscore) >= 20) else print(colored('签到失败！', 'red'))
    exit(0) if (int(ascore) - int(bscore) >= 20) else exit(1)


if "__main__" == __name__:
    sess = login(username, password)
    score(sess)
