# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import jsm
import MySQLdb
import datetime
import config

def main():
	connector = MySQLdb.connect(
		host    = config.db['host'],
		db      = config.db['db'],
		user    = config.db['user'],
		passwd  = config.db['passwd']
	)

	cursor = connector.cursor()

	q = jsm.Quotes()

	dt = datetime.date
	start_date = dt.today() - datetime.timedelta(days = 2)
	end_date   = dt.today() - datetime.timedelta(days = 1)

	cursor.execute("SELECT ccode FROM brands")
	res = cursor.fetchall()
	for r in res:
		try:
			data = q.get_historical_prices(r[0], jsm.DAILY, start_date = start_date, end_date = end_date)
			ts = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			
			for d in data:
				try:
					cursor.execute("INSERT INTO prices(ccode, date, open, high, low, close, volume, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", [r[0], d.date, d.open, d.high, d.low, d.close, d.volume, ts, ts])
					connector.commit()
				except:
					pass
		except:
			pass

	cursor.close()
	connector.close()

if __name__ == '__main__':
	main()
