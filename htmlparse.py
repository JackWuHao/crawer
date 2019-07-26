import requests
import pandas as pd
from bs4 import BeautifulSoup


URL = "http://book.douban.com/latest"

#请求数据
def get_data():
    url = URL
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15"}
    data = requests.get(url,headers=headers)
    # print(data.text)
    return  data



#解析数据
def parse_data(data):
    soup = BeautifulSoup(data.text,'lxml')
    # print(soup)
    books_left = soup.find('ul',{'class':'cover-col-4 clearfix'})
    books_left = books_left.find_all('li')
    books_right = soup.find('ul',{'class':'cover-col-4 pl20 clearfix'})
    books_right = books_right.find_all('li')
    books = list(books_left) + list(books_right)

    img_urls = []
    titles = []
    ratings = []
    authors = []
    details = []
    for book in books:
        img_url = book.find_all('a')[0].find('img').get('src')
        img_urls.append(img_url)
        title = book.find_all('a')[1].get_text()
        titles.append(title)
        print(title)

        #评价星级
        rating = book.find('p',{'class':'rating'}).get_text()
        rating = rating.replace('\n','').replace(' ','')
        ratings.append(rating)


        #作者
        author = book.find('p',{'class':'color-gray'}).get_text()
        author = author.replace('\n','').replace(' ','')
        authors.append(author)

        #图书简介
        detail = book.find_all('p')[2].get_text()
        detail = detail.replace('\n','').replace(' ','')
        details.append(detail)


    print('img_urls:',img_urls)

    print('titles:',titles)

    print('ratings:',ratings)

    print('authors',authors)

    print('details:',details)

    return img_urls,titles,ratings,authors,details


#存储数据
def save_data(imgurls,titles,ratings,authors,details):
    result = pd.DataFrame()
    result['img_urls'] = imgurls
    result['titles'] = titles
    result['ratings'] = ratings
    result['authors'] = authors
    result['details'] = details
    result.to_csv('result.csv',index=None)


def run():
    data = get_data()
    imgurls,titles,ratings,authors,details = parse_data(data)
    save_data(imgurls,titles,ratings,authors,details)

if __name__ == '__main__':
     run()
