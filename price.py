import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import jsm
import mysql.connector
import datetime
import config

def main():
	con = mysql.connector.connect(
		host    = config.db['host'],
		db      = config.db['db'],
		user    = config.db['user'],
		passwd  = config.db['passwd']
	)

	cur = con.cursor()

	q = jsm.Quotes()

	dt = datetime.date
	start_date = dt.today() - datetime.timedelta(days = 3)
	end_date   = dt.today() - datetime.timedelta(days = 1)

	cur.execute("SELECT ccode FROM brands")
	res = cur.fetchall()
	for r in res:
		try:
			data = q.get_historical_prices(r[0], jsm.DAILY, start_date = start_date, end_date = end_date)
			ts = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

			for d in data:
				try:
					cur.execute("INSERT IGNORE INTO prices(ccode, date, open, high, low, close, volume, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", [r[0], d.date, d.open, d.high, d.low, d.close, d.volume, ts, ts])
					con.commit()
				except:
					pass
		except:
			pass

	cur.close()
	con.close()

if __name__ == '__main__':
	main()
