#-*- coding: utf8 -*-
import requests
import base64
import sys,os
import datetime

def getReport(start_date,end_date):

    start_date = start_date + 'T00%3A00%3A00.000'
    end_date = end_date + 'T00%3A00%3A00.000'

    url="http://120.26.121.46:8080/pentaho/api/repos/%3Apublic%3Aglass_store_sale_cost_stock.prpt/report?" \
        "start_date=" + start_date + \
        "&end_date=" + end_date +\
        "&output-target=application%2Fvnd.openxmlformats-officedocument.spreadsheetml.sheet%3Bpage-mode%3Dflow&accepted-page=-1&showParameters=true&renderMode=REPORT&htmlProportionalWidth=false"

    headers = {'Authorization': 'Basic ' + base64.b64encode('admin:admin'),
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    response = requests.post(url,headers=headers)

    now = datetime.datetime.now().strftime('%Y-%m-%d')

    if not os.path.exists('report'):
        os.mkdir('report')
    f = open('report/glass_store_sale_cost_stock-'+str(now)+'.xlsx', 'w')
    f.write(response.content)
    f.close()


def send_mail(send_to, subject, text, files=None):
    import smtplib
    from os.path import basename
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = 'report@jingfree.com'
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    smtp = smtplib.SMTP('smtp.mxhichina.com', 25, None, 300)
    print smtp.login('report@jingfree.com', 'password')

    print smtp.sendmail('report@jingfree.com', send_to, msg.as_string())
    smtp.close()


if "__main__" == __name__:

    date_today = datetime.datetime.now().strftime('%Y-%m-%d')
    getReport('2015-12-01',date_today)

    send_mail(['xiongjun@jingfree.com'], 'glass_store_sale_cost_stock-'+str(date_today), 'glass_store_sale_cost_stock-'+str(date_today), ['report/glass_store_sale_cost_stock-'+str(date_today)+'.xlsx'])
    # send_mail(['xiongjun@jingfree.com','zhangyuhao@jingfree.com','chenzhong@jingfree.com'], 'glass_store_sale_cost_stock-'+str(date_today), 'glass_store_sale_cost_stock-'+str(date_today), ['report/glass_store_sale_cost_stock-'+str(date_today)+'.xlsx'])

