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


# 指定したURLのページを表示する
def printProject(url):
	try:
		resp = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		return False

	src = resp.read()
	soup = BeautifulSoup(src, 'lxml')

	if soup is None:
	    return False

	# プロジェクト名
	pjname = soup.find("h1")

	# タグは:で結合
	tags = soup.find("ul", class_="tags")
	tagstext = tags.find_all("a")
	strs = []
	for it in tagstext:
		strs.append(it.text)
	taglist = ':'.join(strs)


	# 金額
	total = soup.find("dd", class_="Project-visual__condition-dd is-sum")
	total = total.text.replace("円", "").replace(",", "")


	# 目標金額・支援者数
	patrons = soup.find_all("dd", class_="Project-visual__condition-dd u-font-en")
	#patrons = soup.find("dl", class_="Project-visual__condition u-fs_16")
	#patron = patrons.find("dd", class_="Project-visual__condition-dd u-font-en")
	#patron = patrons[1].text.replace("人","").replace(",","")
	#patron = patron.text.replace("人", "").replace(",", "")

	# 見出し
	title = soup.find_all("dt", class_="Project-visual__condition-dt")
	if (title[1].text[-2:] == "者数"):
		patron = patrons[0].text.replace("人", "").replace(",", "")
	elif (title[2].text[-2:] == "者数"):
		patron = patrons[1].text.replace("人", "").replace(",", "")
	else:
		patron = "0"

	# 日
	datetime = soup.find("span", class_="u-fs_14")

	if datetime is None:
		return False

	datestr = datetime.text
	datestr = datestr.replace("このプロジェクトは ", "")
	datestr = datestr.replace(" に成立しました。", "")

	print(url + ",\"" + pjname.text + "\",\"" + taglist + "\",\"" + 
	      patron + "\",\"" + total + "\",\"", datestr+ "\"")

	# 現在時刻
	# now = datetime.datetime.now()
	# print(now.strftime("%Y/%m/%d %H:%M:%S"))
	
	return True
# printProject("https://readyfor.jp/projects/okinawa_toy_museum")
# printProject("https://readyfor.jp/projects/tech-geopolitics")
# printProject("https://readyfor.jp/projects/satoyama2017")
# printProject("https://readyfor.jp/projects/tmoriondrums")
# sys,exit(1)

# readyfor
url = 'https://readyfor.jp/projects/successful?successful_sort_query=successful_desc_accomplished_money'
urlbase = 'https://readyfor.jp'
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

	projects = soup.find_all("article", class_="Entry is-type1 is-achieved Grid__col3 u-mb_40 ")

	# 一画面分
	for proj in projects:
		a = proj.find("a")
		url = a.get('href')
		dbFlag = printProject(urlbase + url)
		time.sleep(1)

	# 次へのリンクを探す
	anchor = soup.find("span", class_="next")
	# なければ終了(最後までクロールした)
	if anchor == None:
		break
	url = anchor.find("a").get("href")
	time.sleep(10)
	resp = urllib.request.urlopen(urlbase + url)
