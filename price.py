# -*- coding: utf-8 -*-

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

	start_date = datetime.date(2014,11,1)
	end_date   = datetime.date.today()

	cursor.execute("SELECT ccode FROM brands")
	res = cursor.fetchall()
	for r in res:
		try:
			data = q.get_historical_prices(r[0], jsm.DAILY, start_date = start_date, end_date = end_date)
			ts = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			[cursor.execute("INSERT INTO prices(ccode, date, open, high, low, close, volume, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", [r[0], d.date, d.open, d.high, d.low, d.close, d.volume, ts, ts]) for d in data]
			connector.commit()
		except:
			print "Error in Price Data ", r[0]

	cursor.close()
	connector.close()

if __name__ == '__main__':
	main()
