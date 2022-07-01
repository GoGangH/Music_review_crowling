import requests
import urllib
from bs4 import BeautifulSoup

def crowling():
    get_search = input('노래 제목을 입력하시오: ')

    url = 'http://izm.co.kr/searchLists.asp?search_tp=8&keywordid=&keyword=' + urllib.parse.quote(get_search)
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

    else : 
        print(response.status_code)
        return

    title = soup.find_all(class_='contents4')
    
    print(title)

def main():
    crowling()

if __name__ == "__main__":
	main()