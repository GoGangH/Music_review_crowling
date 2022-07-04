from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from sqlalchemy import false
import os
import time

def crowling_review(query = "", query2 = ""):
    #step2.검색할 키워드 입력
    query = query.replace(" ", "")
    query2 = query2.replace(" ", "")

    #step3.크롬드라이버로 원하는 url로 접속
    chromeURL = os.getcwd()+'/chromedriver'
    print(chromeURL)
    url = 'http://izm.co.kr/searchLists.asp?search_tp=8&keywordid=&keyword='+query
    driver = webdriver.Chrome(chromeURL)
    driver.get(url)
    time.sleep(2)

    ''' 제목과 가수에 맞는 설명 페이지 이동 '''

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    music_list = driver.find_elements(By.CSS_SELECTOR, '#summary1 > li > table > tbody > tr')

    chk_M = False

    # 페이지 이동
    for i in range(1, len(music_list)+1):
        Music_name = driver.find_element(By.CSS_SELECTOR, f"#summary1 > li.contents4 > table > tbody > tr:nth-child({i}) > td > table > tbody > tr > td:nth-child(1)").text.replace("\n","")
        Music_singer = driver.find_element(By.CSS_SELECTOR, f"#summary1 > li.contents4 > table > tbody > tr:nth-child({i}) > td > table > tbody > tr > td:nth-child(3)").text.replace("\n","")
        if Music_name == query and Music_singer == query2 :
            print("select : " , Music_name, " ", Music_singer)
            driver.find_element(By.XPATH, f"/html/body/ul/li[3]/ul/li[1]/div/ul/li[2]/table/tbody/tr[{i}]/td/table/tbody/tr/td[1]/a").click()
            chk_M=True

    if not chk_M :
        print("제목과 가수를 다시 확인해주세요!")

    time.sleep(1)

    '''페이지 리뷰 설명 가져오기'''

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    review_list = driver.find_element(By.CSS_SELECTOR, f"#summary1 > li.contents3 > article").text.replace("\n", " ")

    return review_list