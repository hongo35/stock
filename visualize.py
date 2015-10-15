import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
# from statsmodels.tsa import arima_model
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

	'''
	date = []
	data = {
		'open':  [],
		'high':  [],
		'low':   [],
		'close': []
	}
	volume = []

	argvs = sys.argv
	argc = len(argvs)

	# 企業コード
	ccode = "1301"
	if argc != 1:
		ccode = argvs[1]

	# 企業名を取得
	market = ""
	corp_name = ""
	cur.execute("SELECT market,name FROM brands WHERE ccode = %s", [ccode])
	res = cur.fetchall()
	for r in res:
		market    = "【" + r[0] + "】"
		corp_name = r[1]

	# 株価を取得
	cur.execute("SELECT date,open,high,low,close,volume FROM prices WHERE ccode = %s", [ccode])
	res = cur.fetchall()
	for r in res:
		try:
			date.append(r[0].strftime("%Y-%m-%d"))
			data['open'].append(r[1])
			data['high'].append(r[2])
			data['low'].append(r[3])
			data['close'].append(r[4])
			volume.append(r[5])
		except:
			pass

	series = pd.Series(data['close'], index=date)
	series.plot(title=(market + corp_name))
	plt.show()
	'''

	'''
	# ARIMAモデルで時系列予測
	results = arima_model.ARIMA(data['close'],order=[4,0,0]).fit()

	plt.clf()
	plt.plot(data['close'])
	plt.plot(results.predict(start=0,end=(len(data['close']) + 5)))
	plt.legend(['data', 'predicted'])

	# 可視化
	#fig, axes = plt.subplots(2,1)
	#data_frame = pd.DataFrame(data, index=date)
	series = pd.Series(data['close'], index=date)
	#series.plot(title=(market + corp_name))
	pd.rolling_mean(series, 4).plot(style='--', c='r')
	plt.legend(['data', 'predicted(ARIMA)', 'moving average'])

	#volume_series = pd.Series(volume, index=date)
	#volume_series.plot(kind='bar', ax=axes[1])
	plt.show()
	'''

if __name__ == '__main__':
	main()
