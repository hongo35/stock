import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import config
import mysql.connector
import datetime
import requests
from bs4 import BeautifulSoup

def main():
	con = mysql.connector.connect(
		host    = config.db['host'],
		db      = config.db['db'],
		user    = config.db['user'],
		passwd  = config.db['passwd'],
		charset = "utf8"
	)

	cur = con.cursor()

	res = requests.get("http://news.yahoo.co.jp/hl?c=biz")
	soup = BeautifulSoup(res.text)

	news_list = soup.find("ul", class_="listBd").find_all("li")
	for li in news_list:
		news = li.find("p", class_="ttl").find("a")
		
		subject = news.text
		url     = news.get("href")
		news_id = url.split("a=")[1]
		source  = li.find("p", class_="source").find("span", class_="cp").text
		ts      = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

		try:
			cur.execute("INSERT INTO articles(id,subject,url,source,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s)", [news_id,subject,url,source,ts,ts])
			con.commit()
		except:
			pass

	cur.close()
	con.close()

if __name__ == '__main__':
	main()
