import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

#rank, subject, name
for song in songs:
    rank = song.select_one('td.number')
    subject = song.select_one('td.info > a.title.ellipsis')
    name = song.select_one('td.info > a.artist.ellipsis')
    # a = rank.text.strip().splitlines()[0]
    a = rank.text.split()[0].strip()
    b = subject.text.strip().splitlines()[0]
    c = name.text.strip().splitlines()[0]
    db.song.insert_one({'rank':a, 'subject':b, 'name':c})


