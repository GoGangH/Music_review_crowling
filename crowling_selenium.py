from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

#step2.검색할 키워드 입력
query = input('검색할 키워드를 입력하세요: ')
query2 = input('가수명을 입력하세요: ')

#step3.크롬드라이버로 원하는 url로 접속
chromeURL = os.getcwd()+'/chromedriver'
print(chromeURL)
url = 'http://izm.co.kr/searchLists.asp?search_tp=8&keywordid=&keyword='+query
driver = webdriver.Chrome(chromeURL)
driver.get(url)
time.sleep(3)

# continue_link = driver.find_element_by_partial_link_text(query2)
# continue_link.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

titles = soup.select('#summary1 > li > table > tbody > tr')

print(titles)