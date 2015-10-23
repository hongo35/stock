import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import mysql.connector as mysql
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import config

def main():
	con = mysql.connect(
		host    = config.db['host'],
		db      = config.db['db'],
		user    = config.db['user'],
		passwd  = config.db['passwd']
	)
	cur = con.cursor(dictionary=True)

	start_date = datetime.strptime('2015-01-01', '%Y-%m-%d')
	end_date   = datetime.strptime('2015-02-01', '%Y-%m-%d')

	data = {}
	for d in range((end_date - start_date).days):
		date = (start_date + timedelta(d)).strftime('%Y-%m-%d')

		data[date] = {
			'open': 0,
			'high': 0,
			'low': 0,
			'close': 0,
			'volume': 0
		}

	# 企業コード
	ccode = 1301

	# 企業名を取得
	market = ''
	corp_name = ''
	cur.execute("SELECT market,name FROM brands WHERE ccode = %s" % (ccode))
	for r in iter(cur):
		market    = "【" + r['market'] + "】"
		corp_name = r['name']

	# 株価を取得
	cur.execute("SELECT date,open,high,low,close,volume FROM prices WHERE ccode = %s" % (ccode))
	for r in iter(cur):
		date = r['date'].strftime('%Y-%m-%d')

		try:
			data[date]['open'] = r['open']
			data[date]['high'] = r['high']
			data[date]['low'] = r['low']
			data[date]['close'] = r['close']
			data[date]['volume'] = r['volume']
		except:
			pass

	dates = []
	data_frame = {
		'open': [],
		'close': []
	}
	for r in sorted(data):
		dates.append(r)
		data_frame['open'].append(data[r]['open'])
		data_frame['close'].append(data[r]['close'])

	series = pd.DataFrame(data_frame, index=dates)
	series.plot(title=(market + corp_name))
	plt.show()

if __name__ == '__main__':
	main()
