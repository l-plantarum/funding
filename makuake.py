#!/usr/bin/python3
# coding=utf-8

import time
import urllib.request
from bs4 import BeautifulSoup
import sys
import re
import datetime
import json
import syslog


# 指定した記事を開き，取り消し済みならNoneを返す
def urlopen(url):
	try:
		resp = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		return None
	else:
		return resp

# 指定したURLのページを表示する
def printProject(url, stat, total, goal):
	resp = urllib.request.urlopen(url)
	src = resp.read()
	soup = BeautifulSoup(src, 'lxml')
	heroBase = soup.find("div", class_="heroBase")
	heroBtmBase =  soup.find("div", class_="heroBtmBase")

	# プロジェクト名
	pjname = heroBtmBase.find("h2", class_="projectTtl")

	# カテゴリ
	category = heroBtmBase.find("div", class_="project_category")
	cat = category.find("a").text.strip()

	# 地域(あれば)
	district = heroBtmBase.find("span", class_="location-name")

	if (district != None) :
		dist = district.text
	else:
		dist = ""

	print(url + "," + pjname.text + "," + cat + "," + dist + "," +
	      stat + "," + total + "," + goal + ",")

	# 現在時刻
	# now = datetime.datetime.now()
	# print(now.strftime("%Y/%m/%d %H:%M:%S"))
	
	return True


# Makuake
url = 'https://www.makuake.com/discover/projects/search/'
urlbase = 'https://www.makuake.com'

# トップページの情報を取得
resp = urllib.request.urlopen(url)

maxpage = int(sys.argv[1])
curpage = 1

# 最後までクロールしたらbreakする
while True:
	if curpage >= maxpage:
		break
	src = resp.read()
	soup = BeautifulSoup(src, 'lxml')

	projects = soup.find_all("li", class_="pj-box-li")

	# 一画面分
	for proj in projects:
		a = proj.find("a")
		url = a.get('href')
		
		# 残り日数
		st = proj.find("div", class_="media-middle-time")
		val = st.find("p")
		if val.text != '終了':
			continue

		# 目標金額
		goal = proj.find("div", class_="media-middle-money").find("p")
		
		# 目標達成率
		rate = proj.find("div", class_="media-low-bar-num")

		# 100%より下なら次に
		if len(rate.text) < 4:
			continue
		dbFlag = printProject(urlbase + url, val.text, goal.text, rate.text)
		time.sleep(1)

	# 次へのリンクを探す
	anchor = soup.find("a", class_="pageRight")
	# なければ終了(最後までクロールした)
	if anchor == None:
		break
	url = anchor.get("href")
	time.sleep(10)
	resp = urllib.request.urlopen(urlbase + url)
