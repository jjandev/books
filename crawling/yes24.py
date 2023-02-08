from bs4 import BeautifulSoup
import requests
import json
import csv
from datetime import datetime
from tqdm import tqdm
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


    def get_list(self, category_code: str, sumgb: str):      
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

        with open(f'./book_list/{self.category_code}-sumgb{self.sumgb}-{datetime.now().strftime("%Y-%m-%d")}.json', 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False)




    # def get_best_seller(category_code: str = '001001003'):
    #     """
    #     category_code
    #     - yes24 카테고리 분류 코드
    #     - default : IT 모바일 (001001003)
    #     """
    

    
if __name__ == "__main__":
    yes24 = Yes24()
    it_books = ["001001003027", "001001003028", "001001003024", "001001003023", 
                "001001003021", "001001003029", "001001003020", "001001003026", 
                "001001003031", "001001003030", "001001003019", "001001003022", "001001003025"]
    for book in it_books:
        yes24.get_list(book, '06')
