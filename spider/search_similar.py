# -*- coding: utf-8 -*-
"""
Created on 2021-10-15 09:42:05
---------
@summary:
---------
@author: soda
"""


import feapder
from pathlib import Path
import pandas as pd
import csv
from util import *
from time import sleep

class SearchSimilar(feapder.AirSpider):

    def __init__(self, key_word, iterator_count, thread_count=1):
        super().__init__(thread_count=thread_count)
        self.page_count = 100
        self.iterator_count = iterator_count
        self.key_word = key_word
        self.folder = Path(self.key_word)
        if self.iterator_count == 1:
            self.last_file = self.folder / 'search_keyword.csv'
        else:
            self.last_file = self.folder / f'search_similar_{self.iterator_count-1}.csv'

        self.now_file = self.folder / f'search_similar_{self.iterator_count}.csv'
        create_folder(self.folder)
        create_csv(self.now_file)
        self.f = open(self.now_file, 'a+', encoding='utf-8_sig', newline='')
        self.csv_writer = csv.writer(self.f)

        self.is_similar, self.not_similar = self.get_is_similar()
        self.find_goods = []
        self.write_datas = []


    def get_is_similar(self):
        is_similar,not_similar = [], []
        df = pd.read_csv(self.last_file, encoding='utf-8_sig', keep_default_na=False)
        for i in range(len(df)):
            data = df.iloc[i].tolist()
            if df.loc[i, 'similar-flag'] == 0:
                not_similar.append(df.loc[i, 'itemid-shopid-catid'])
                data[1] = 1
            self.csv_writer.writerows([data])
        self.f.flush()
        is_similar = df['itemid-shopid-catid'].tolist()
        
        print(f'>>> 共有{len(df)}个商品，已查找相似的有{len(df)-len(not_similar)}个，剩余{len(not_similar)}个需要查找')
        return is_similar, not_similar

    def get_params(self, item_shop_cat_id, i):
        itemid, shopid, catid = item_shop_cat_id.split('-')
        return {
            "bundle": "find_similar_product_sc",
            "catid": catid,
            "item_card": "2",
            "itemid": itemid,
            "limit": f'{self.page_count}',
            "offset": f'{i*self.page_count}',
            "shopid": shopid
        }

    def start_requests(self):
        url = 'https://xiapi.xiapibuy.com/api/v4/recommend/recommend'
        for item_shop_cat_id in self.not_similar:
            index = 0
            params = self.get_params(item_shop_cat_id, index)
            yield feapder.Request(url, params=params, headers=get_xiapi_match(params), index=index, item_shop_cat_id=item_shop_cat_id)


    def parse(self, request, response):
        items = response.json.get('data', {}).get('sections', [{}])[0].get('data', {}).get('item', [])
        if items:
            datas = list(map(get_info, items))
            data_count = 0
            for data in datas:
                if data[0] not in self.is_similar and data[0] not in self.find_goods and self.key_word in data[2]:
                    data_count += 1
                    self.find_goods.append(data[0])
                    self.write_datas.append(data)
            print(f'{request.index}--->{data_count}')

            params = self.get_params(request.item_shop_cat_id, request.index+1)
            #yield feapder.Request(request.url, params=params, headers=get_xiapi_match(params), index=request.index+1, item_shop_cat_id=request.item_shop_cat_id)

    def __del__(self):
        self.csv_writer.writerows(self.write_datas)
        self.f.flush()
        self.f.close()
        df = pd.read_csv(self.now_file, encoding='utf-8_sig', keep_default_na=False)
        df = df.drop_duplicates()
        data_increase = len(df) - len(self.is_similar)
        df.to_csv(self.now_file, index=False, encoding='utf-8_sig')
        print(f'>>> 通过第{self.iterator_count}次相似迭代，一共新增{data_increase}件商品,新增商品率为{data_increase*100/len(df):.4f}%')

if __name__ == "__main__":
    iterator_count = eval(input('iterator_count: '))
    key_word = '菜刀'
    SearchSimilar(key_word=key_word, iterator_count=iterator_count, thread_count=10).start()
    sleep(30)