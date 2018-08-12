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


statere = re.compile(u"\S+人の支援により(?P<money>\S+)の資金を集め、(?P<limit>\S+)に募集を終了しました")

# 指定した記事を開き，取り消し済みならNoneを返す
def urlopen(url):
	try:
		resp = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		return None
	else:
		return resp

# 指定したURLのページを表示する
def printProject(url, customFlag):
	resp = urllib.request.urlopen(url)
	src = resp.read()
	soup = BeautifulSoup(src, 'lxml')

	# タイトル
	h1 = soup.find("h1")
	if h1.get("class") is None:
		title = h1.text
		tagline = soup.find("div", class_="subtitle center row")
		if tagline is not None:
			tags = tagline.find_all("a")
	else:
		pjinfo = soup.find("div", class_="header_top")
		title = pjinfo.find("h2").text
		tags = pjinfo.find_all("a")


	closestate = soup.find("div", class_="records-in inner")
	if closestate is None:
		closestate = soup.find("section", class_="status")
		if closestate is None:
			states = soup.find_all("div", class_="project_status")
			closestate = states[1]
	else:
		tags = closestate.find_all("a")

	strs = []
	for it in tags:
		strs.append(it.text.strip())
	taglist = ':'.join(strs)

	# 金額
	if closestate['class'][0] == "project_status":
		params = closestate.find_all("strong")
		total = params[2].text
		datestr = params[3].text
	else:
		m = statere.match(closestate.text)
		total = m.groupdict()['money']
		datestr = m.groupdict()['limit']

	print(url + ",\"" + title + "\",\"" + taglist + "\",\"" + 
	      total + "\",\"", datestr+ "\"")

	# 現在時刻
	# now = datetime.datetime.now()
	# print(now.strftime("%Y/%m/%d %H:%M:%S"))
	
	return True


#dbFlag = printProject('https://camp-fire.jp/projects/view/5795', False)
#dbFlag = printProject('https://camp-fire.jp/projects/view/53685', False)
#dbFlag = printProject('https://camp-fire.jp/projects/view/34653', False)
#dbFlag = printProject('https://camp-fire.jp/projects/view/86991', False)
#sys.exit(1)

# camp-fire
url = 'https://camp-fire.jp/projects/most-funded'
urlbase = 'https://camp-fire.jp'

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

	projects = soup.find_all("div", class_="box")

	# 一画面分
	for proj in projects:
		boxclass = proj.get('class')
		a = proj.find("a")
		url = a.get('href')
		if len(boxclass) == 1 or boxclass[1] == '':
			per = proj.find("div", class_="success-summary")
			if per is None:
				continue
			# non custom
			dbFlag = printProject(urlbase + url, False)
		else:
			# custom
			dbFlag = printProject(urlbase + url, True)
		time.sleep(1)

	# 次へのリンクを探す
	anchor = soup.find("a", rel="next")
	# なければ終了(最後までクロールした)
	if anchor == None:
		break
	url = anchor.get("href")
	time.sleep(10)
	resp = urllib.request.urlopen(urlbase + url)
