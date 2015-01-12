# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa import arima_model
import datetime
import config

class Stock:
	def __init__(self):
		self.con = MySQLdb.connect(
			host    = config.db['host'],
			db      = config.db['db'],
			user    = config.db['user'],
			passwd  = config.db['passwd'],
			charset = "utf8"
		)
		self.cursor = self.con.cursor()

	def wr(self, span):
		self.cursor.execute("SELECT brands.ccode,brands.name,finances.per,finances.pbr,finances.price_min FROM brands INNER JOIN finances ON brands.ccode = finances.ccode")
		brands = self.cursor.fetchall()
		for b in brands:
			data = {
				'open': [],
				'high': [],
				'low': [],
				'close': []
			}

			self.cursor.execute("SELECT date,open,high,low,close,volume FROM prices WHERE ccode = %s ORDER BY date", [b[0]])
			res = self.cursor.fetchall()
			for r in res:
				try:
					data['open'].append(r[1])
					data['high'].append(r[2])
					data['low'].append(r[3])
					data['close'].append(r[4])
				except:
					pass

			highest      = 0
			lowrst       = 0
			latest_close = 0
			try:
				highest      = max(data['high'][(len(data['high']) - span):])
				lowest       = min(data['low'][(len(data['low']) - span):])
				latest_close = data['close'][-1]
			except:
				pass

			if (highest - lowest) != 0:
				wr    = (highest - latest_close) * 100 / (highest - lowest)
				per   = b[2]
				pbr   = b[3]
				price = b[4]
				
				# 条件
				if wr == 100 and per < 20 and price < 100000:
					print "%s,%s,%s,%s,%s,%s" % (b[0], b[1], per, pbr, price, latest_close)

if __name__ == '__main__':
	s = Stock()
	s.wr(30)
