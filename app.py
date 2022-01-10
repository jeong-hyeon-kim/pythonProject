import uuid
import re
import pymongo
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient

# todo client를 ec2 host로 변경!
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.mini

# 이 조건을 달지 않으면, css같은 사항 변화를 12시간마다 체크한다. 즉 디버깅모드에서는 불편하므로, 디버깅시에는 1초로 변경하는 것.
if app.config['DEBUG']:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

from datetime import datetime

# current_year = datetime.now().year
# current_month = datetime.now().month
# current_day = datetime.now().day
#
# today = f"{current_year}년 {current_month}월 {current_day}일"


# article1 = {
#     "_id": uuid.uuid4().hex, #고유 식별자 만들어주는 거
#     "writer_id":"skjh0807s",
#     "writer_name": "겨울스누피",
#     "post_date": today,
#     "album_title": "폐허가 된다 해도",
#     "album_singer": "이승윤",
#     "album_image":"https://musicmeta-phinf.pstatic.net/album/006/710/6710242.jpg?type=r480Fll&v=20220105144508",
#     "article_url": "https://vibe.naver.com/track/51895397",
#     "article_description": "진짜 너무 좋아하는 노래!!!",
#     "like":0
# }

# @app.route('/<word>')
# def jinja2test(word):
#     return render_template('index.html', name=word)

# 홈 화면 주기
@app.route('/')
def home():
    return render_template('index.html')


# API - home(index.html)에서 연결된 부분들
@app.route('/api/home/articles', methods=['GET'])
def all_articles():
    all_articles = list(db.articles.find({}, {}).sort('like', pymongo.DESCENDING))
    return jsonify({'all_articles': all_articles})


@app.route('/api/home/search_article', methods=['GET'])
def keyword_search():
    keyword = request.args.get('keyword')
    print(keyword)
    found_articles = list(db.articles.find({'$or': [{'album_singer':{'$regex': keyword}}, {'album_title':{'$regex': keyword}}]},{}))
    return jsonify({'found_articles': found_articles})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)