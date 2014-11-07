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

	cursor.execute("SELECT ccode FROM brands")
	res = cursor.fetchall()
	for r in res:
		try:
			finance_data = q.get_finance(r[0])
			
			ts = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			cursor.execute("INSERT INTO finances(ccode, market_cap, shares_issued, dividend_yield, dividend_one, per, pbr, eps, bps, price_min, round_lot, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [r[0], finance_data.market_cap, finance_data.shares_issued, finance_data.dividend_yield, finance_data.dividend_one, finance_data.per, finance_data.pbr, finance_data.eps, finance_data.bps, finance_data.price_min, finance_data.round_lot, ts, ts])
			connector.commit()
		except:
			print "Error in Financial Data ", r[0]

	cursor.close()
	connector.close()

if __name__ == '__main__':
	main()
