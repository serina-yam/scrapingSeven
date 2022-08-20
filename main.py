# -*- coding: utf-8 -*-
import logging
import requests
from bs4 import BeautifulSoup as bs4
import re
import csv

# ロガーを取得する
logger = logging.getLogger(__name__)


"""
セブンイレブンの「今週の新商品」から
情報を取得してcsvに格納

作成日：2022年8月20日
"""

# 「セブンイレブン」url
# トップ 商品のご案内 今週の新商品 関東
base_url = 'https://www.sej.co.jp/products/a/thisweek/area/kanto/1/l100/'
r = requests.get(base_url)
soup = bs4(r.text, 'lxml')

csvlist = []
csvlist.append(["タイトル", "脂肪", "栄養成分"])  # カラム名設定

print("書き込みを開始します")

items = soup.select(".item_ttl > p > a")
# 上映日・タイトル・スコアをリストに格納
for item in items:
    next_url = 'https://www.sej.co.jp' + item.get('href')
    # print(next_url)
    rr = requests.get(next_url)
    soupsoup = bs4(rr.text, 'lxml')

    title = soupsoup.select_one('.item_ttl > h1').text  # タイトル
    nutrition = soupsoup.select_one(
        '.allergy > table > tbody > tr:nth-child(2) > td').text  # 栄養成分
    fat = re.findall('脂肪.*、', nutrition).replace(' 脂質：',
                                                 '').replace('g', '')  # 脂肪 栄養成分から数値のみ抽出

    csvlist.append([title, fat, nutrition])

# CSVファイルを開く。ファイルがなければ新規作成する。
f = open("セブン今週の新商品.csv", "w")
writecsv = csv.writer(f, lineterminator='\n')

# 出力
writecsv.writerows(csvlist)

# CSVファイルを閉じる。
f.close()

print("書き込みが完了しました")
