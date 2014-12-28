# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import config
import MySQLdb as mdb
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email import charset

def main():
	con = mdb.connect(
		host    = config.db['host'],
		db      = config.db['db'],
		user    = config.db['user'],
		passwd  = config.db['passwd'],
		charset = "utf8"
	)

	mail_body = ""
	cron_ts = (datetime.datetime.today() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d 10:30:00")

	cursor = con.cursor()
	cursor.execute("SELECT * FROM articles WHERE created_at > %s ORDER BY created_at", [cron_ts])
	res = cursor.fetchall()
	for r in res:
		mail_body += "<a href='%s'>%s</a>[%s]<br/>" % (r[2], r[1], r[3])

	mcon = smtplib.SMTP('localhost')
	mcon.set_debuglevel(True)

	cset = 'utf-8'  # <---------------(文字セットの設定だよ)

	message = MIMEText(mail_body, 'html', cset)
	message['Subject'] = Header(u'[News][Stock]ヤフー株式ニュースまとめ', cset)
	message['From']    = config.mail['from']
	message['To']      = config.mail['to']

	mcon.sendmail(config.mail['from'], [config.mail['to']], message.as_string()) 
	mcon.close()

	cursor.close()
	con.close()

if __name__ == '__main__':
	main()
