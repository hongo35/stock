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

	"""Brandの取得"""
	brand = jsm.Brand()
	ids = brand.IDS # 業種コードのリスト

	brand_list = []
	for industory_code in ids.keys():
		industory_name = ids[industory_code]
		brand_data = q.get_brand(industory_code) # 業種ごとの属性情報の取得を行う

		for data in brand_data:
			ts = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			cursor.execute("INSERT INTO brands(ccode, industory_code, industory_name, market, name, info, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (data.ccode, industory_code, industory_name, data.market, data.name, data.info, ts, ts))
			connector.commit()

	cursor.close()
	connector.close()

if __name__ == '__main__':
	main()
