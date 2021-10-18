# -*- coding: utf-8 -*-
"""
Created on 2021-10-15 09:41:52
---------
@summary:
---------
@author: soda
"""

import feapder
from pathlib import Path
import csv
from util import *


class SearchKeyword(feapder.AirSpider):

    def __init__(self, key_word, thread_count=20):
        super().__init__(thread_count=thread_count)

        self.key_word = key_word
        self.folder = Path(self.key_word)
        self.page_count = 100
        self.now_file = self.folder / 'search_keyword.csv'
        create_folder(self.folder)
        create_csv(self.now_file)
        self.f = open(self.now_file, 'a+', encoding='utf-8_sig', newline='')
        self.csv_writer = csv.writer(self.f)
        self.find_goods = []

    def get_params(self, i):
        return {
            'by': 'relevancy',
            'keyword': self.key_word,
            'limit': f'{self.page_count}',
            'newest': f'{i * self.page_count}',
            'order': 'desc',
            'page_type': 'search',
            'scenario': 'PAGE_GLOBAL_SEARCH',
            'version': '2'
        }

    def start_requests(self):
        url = 'https://xiapi.xiapibuy.com/api/v4/search/search_items'
        index = 0
        params = self.get_params(index)
        yield feapder.Request(url, params=params, headers=get_xiapi_match(params), index=index)

    def parse(self, request, response):
        items = response.json.get('items', [])
        if items:
            items = map(lambda x: x.get('item_basic', {}), items)
            datas = list(map(get_info, items))
            data_count = 0
            for data in datas:
                if data[0] not in self.find_goods and self.key_word in data[2]:
                    self.find_goods.append(data[0])
                    self.csv_writer.writerows([data])
                    data_count += 1
            print(f'{request.index}--->{data_count}')
            self.f.flush()

            params = self.get_params(request.index + 1)
            # yield feapder.Request(request.url, params=params, headers=get_xiapi_match(params), index=request.index+1)

    def __del__(self):
        self.f.close()
        print(f'>>> 通过搜索，一共找到{len(self.find_goods)}件商品')


if __name__ == "__main__":
    key_word = '菜刀'
    demo = SearchKeyword(key_word=key_word, thread_count=1)
    demo.start()
    # from time import sleep
    # sleep(8)
    #print(f'>>> 通过搜索，一共找到{len(demo.find_goods)}件商品')


