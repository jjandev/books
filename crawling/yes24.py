from bs4 import BeautifulSoup
import requests
import json
import csv
from datetime import datetime
from tqdm import tqdm
import os
import asyncio
# class GetData:
#     def __init__(self, func: function):
#         self.func = func

#     def __call__(self, *args, **kwargs):
#         self.func(*args, **kwargs)
        
        

class Yes24:
    """
    yes24 베스트셀러 데이터 수집

    categories : yes24 카테고리 분류 코드
    category_datails : yes24 카테고리 세부 분류 코드

    URL : yes24 베스트셀러 url
    """

    with open('./category/yes24_categories.json', 'r') as f:
        categories = json.load(f)
    with open('./category/yes24_category_details.json', 'r') as f:
        category_details = json.load(f)


    def get_rank_list_tmp(self, category_code: str, sumgb: str):      
        dic = dict()

        pnum = 1
        rank = 1
        self.category_code = category_code
        self.sumgb = sumgb
        while tqdm(True):
            BASE_URL = f'http://www.yes24.com/24/Category/BestSeller?CategoryNumber={self.category_code}&sumgb={self.sumgb}&PageNumber={pnum}'

            req = requests.get(BASE_URL).text

            soup = BeautifulSoup(req, 'html.parser')

            table = soup.find('table', {'class':'list'}).find_all('tr')

            if len(table) == 0:
                break

            for i in range(0, len(table), 2):
                temp = table[i].find('td', {'class':'goodsTxtInfo'}).select('p:nth-child(1) > a:nth-child(1)')[0]
                title = temp.text

                product_id = temp.attrs['href'].split('/')[-1]
                dic[str(rank)] = {'title':title, 'productId': product_id}
                rank += 1
            pnum += 1
            # break
        # print(dic)

        with open(f'./yes24_data/rank_list_tmp/yes24-{self.category_code}-sumgb{self.sumgb}-{datetime.now().strftime("%Y%m%d")}.json', 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False)

    # async def fetch(self, url):
    #     self.URL = url
    #     soup = BeautifulSoup(requests.get(self.URL).text, 'html.parser')

    def get_rank_list(self, LOAD_PATH, SAVE_PATH, file_list):
        self.LOAD_PATH = LOAD_PATH
        self.SAVE_PATH = SAVE_PATH
        self.file_list = file_list

        for i in self.file_list:
            if not i.endswith('.json'):
                continue
            file = os.path.join(self.LOAD_PATH, i)
            with open(file, 'r', encoding='utf-8') as f:
                json_file = json.load(f)
            # print(json_file)
            # print(json_file.keys())
            ls = []
            zzzz = []
            cnt = 1
            for k in tqdm(json_file.keys()):
                # if int(k) != 61:
                #     continue
                # if cnt == 10:
                #     break
                URL = f"http://www.yes24.com/Product/Goods/{json_file[k]['productId']}"

                soup = BeautifulSoup(requests.get(URL).text, 'html.parser')


                # async def fetch(url):
                #     request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})    # UA가 없으면 403 에러 발생
                #     response = await loop.run_in_executor(None, urlopen, request)    # run_in_executor 사용
                #     page = await loop.run_in_executor(None, response.read)           # run in executor 사용
                #     return len(page)
                
                # async def main():
                #     futures = [asyncio.ensure_future(fetch(url)) for url in urls]
                #                                                         # 태스크(퓨처) 객체를 리스트로 만듦
                #     result = await asyncio.gather(*futures)                # 결과를 한꺼번에 가져옴
                #     print(result)


                # isbn = soup.find('div', {'class':'infoSetCont_wrap'}).find_all('td')[2].text

                isbn = soup.select_one('.infoSetCont_wrap > .yesTb').find_all('td')[2].text
                ls.append({'rank': k, 'title':json_file[k]['title'], 'isbn':isbn})
                # print({'rank': k, 'title':json_file[k]['title'], 'isbn':isbn})


            with open(f'{self.SAVE_PATH}/{i}', 'w', encoding='utf-8') as ff:
                json.dump(ls, ff, ensure_ascii=False)
            # break







    # def get_best_seller(category_code: str = '001001003'):
    #     """
    #     category_code
    #     - yes24 카테고리 분류 코드
    #     - default : IT 모바일 (001001003)
    #     """
    

    
if __name__ == "__main__":
    yes24 = Yes24()
    # it_books = ["001001003", "001001003027", "001001003028", "001001003024", "001001003023", 
    #             "001001003021", "001001003029", "001001003020", "001001003026", 
    #             "001001003031", "001001003030", "001001003019", "001001003022", "001001003025"]
    # for book in it_books:
    #     yes24.get_rank_list_tmp(book, '06')

    LOAD_PATH = './book_data/yes24'
    SAVE_PATH = './yes24_data/rank_list'
    file_list = os.listdir('./book_data/yes24')
    yes24.get_rank_list(LOAD_PATH, SAVE_PATH, file_list)
