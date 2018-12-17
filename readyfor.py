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
def printProject(url):
	resp = urllib.request.urlopen(url)
	src = resp.read()
	soup = BeautifulSoup(src, 'lxml')
	article = soup.find("article", class_="Page-body")
        # 終了プロジェクト
	if article is None:
	    return False

	# プロジェクト名
	pjname = article.find("h1")

	# タグは:で結合
	tags = article.find("ul", class_="tags")
	tagstext = tags.find_all("a")
	strs = []
	for it in tagstext:
		strs.append(it.text)
	taglist = ':'.join(strs)

	# 金額
	total = article.find("dd", class_="Project-visual__condition-dd is-sum")

	# 日
	datetime = article.find("span", class_="u-fs_14")
	datestr = datetime.text
	datestr = datestr.replace("このプロジェクトは ", "")
	datestr = datestr.replace(" に成立しました。", "")


	print(url + ",\"" + pjname.text + "\",\"" + taglist + "\",\"" + 
	      total.text + "\",\"", datestr+ "\"")

	# 現在時刻
	# now = datetime.datetime.now()
	# print(now.strftime("%Y/%m/%d %H:%M:%S"))
	
	return True


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
