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

	cur.execute("SELECT ccode FROM brands")
	res = cur.fetchall()
	for r in res:
		try:
			finance_data = q.get_finance(r[0])

			market_cap     = finance_data.market_cap
			shares_issued  = finance_data.shares_issued
			dividend_yield = finance_data.dividend_yield
			dividend_one   = finance_data.dividend_one
			per            = finance_data.per
			pbr            = finance_data.pbr
			eps            = finance_data.eps
			bps            = finance_data.bps
			price_min      = finance_data.price_min
			round_lot      = finance_data.round_lot

			ts = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			cur.execute("INSERT INTO finances(ccode, market_cap, shares_issued, dividend_yield, dividend_one, per, pbr, eps, bps, price_min, round_lot, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE market_cap = %s, shares_issued = %s, dividend_yield = %s, dividend_one = %s, per = %s, pbr = %s, eps = %s, bps = %s, price_min = %s, round_lot = %s, updated_at = %s", [r[0], market_cap, shares_issued, dividend_yield, dividend_one, per, pbr, eps, bps, price_min, round_lot, ts, ts, market_cap, shares_issued, dividend_yield, dividend_one, per, pbr, eps, bps, price_min, round_lot, ts])
			con.commit()
		except:
			pass

	cur.close()
	con.close()

if __name__ == '__main__':
	main()
