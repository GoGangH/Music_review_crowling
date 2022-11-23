import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import json

def imglink_crow(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    html = requests.get('https://www.genie.co.kr/search/searchSong?query='+query, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')
    html.close()

    # trs 라는 변수에 아래 경로에 있는 모든 tr 태그 안에 있는 정보 가져오기
    img_list = soup.findAll("table", {'class':'list-wrap'})

    list = []
    for data in img_list:
        # 제목+썸내일 영역 추출
        list.extend(data.findAll("tr", {'class':'list'}))
    for li in list:
        img = li.find('img')
        img_src = img['src']
        break

    img_link = 'image.genie.co.kr'+img_src
    print(query, img_link)
    return img_link

directory_path = 'data/'
tag=[]
df = pd.read_json(directory_path+'meta_list.json')
df2 = pd.read_json(directory_path+'music_tag.json')
for topic, mood, situation, genre, date in zip(df2['topic'], df2['mood'], df2['situation'], df['album_genre'], df['release_date']):
    m = date[5:6]
    if date[6] != '.':
        m=date[5:7]

    if 2 < int(m) < 6:
        date = '봄'
    elif 5 < int(m) < 9:
        date = '여름'
    elif 8 < int(m) < 12:
        date = '가을'
    else:
        date = '겨울'
    tag.append(topic + ' ' + mood + ' ' + situation + ' ' + genre + ' ' + date)

df['tag'] = tag

#img url 크롤링 및  저장
img_url = []
for title in df['track_title']:
    img_url.append(imglink_crow(title))
    time.sleep(5)

df['img_url'] = img_url

#불 필요 열 제거
df = df.drop(['album_genre'], axis = 1)
df = df.drop(['release_date'], axis = 1)
df = df.drop(['album_title'], axis = 1)
df = df.drop(['track_id'], axis = 1)
df = df.drop(['play_time'], axis = 1)

df = df.rename(columns={'artists':'artist'})
df = df.rename(columns={'track_title':'title'})


#json형식으로 load
json_data = df.to_json(force_ascii=False, orient = 'records', indent=4)
parsed = json.loads(json_data)

#django용 json 저장
body = ""
for i in parsed:
    body = body + json.dumps(i, ensure_ascii=False) + '\n'

f = open(directory_path + 'music.json', 'w')
f.write(body)
f.close()

#elastic용 json 저장
body = ""
count = 1
for i in parsed:
    body = body + json.dumps({"index": {"_index": "music", "_id": count}}) + '\n'
    body = body + json.dumps(i, ensure_ascii=False) + '\n'
    if count == 1:
        print(body)
    count += 1

f = open(directory_path + 'elastic_input.json', 'w')
f.write(body)
f.close()
