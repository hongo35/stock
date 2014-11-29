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

	start_date = datetime.date(2014,10,1)
	end_date   = datetime.date(2014,11,4)

	cursor.execute("SELECT ccode FROM brands where ccode = 1821")
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
