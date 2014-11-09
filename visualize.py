# -*- coding:utf-8 -*-

import MySQLdb
import pandas as pd
import numpy as np
import pandas.io.sql as psql
import matplotlib.pyplot as plt
import config

con = MySQLdb.connect(
	host    = config.db['host'],
	db      = config.db['db'],
	user    = config.db['user'],
	passwd  = config.db['passwd']
)

sql = "SELECT date,open,close FROM prices where ccode = 1301 order by date"

df = psql.read_sql(sql, con)
x = []
dic = []
t = []
for index, row in df.iterrows():
	x.append(row.close)
	dic.append({'open': row.open, 'close': row.close})
	t.append(row.date.strftime('%Y-%m-%d'))

con.close()

# Seriesのプロッティング
#ts = pd.Series(x, t)
#ts.plot()
#plt.show()

# DataFrameのプロッティング
ts = pd.DataFrame(dic, t)
ts.plot()
plt.show()
