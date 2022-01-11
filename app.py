import uuid
from datetime import datetime

import pymongo
from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

from pymongo import MongoClient

# TODO EC2랑 연결된 mongoDb로 변경
client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://test:test@localhost', 27017)

db = client.mini

# 다른 API 경로들 파일 연결
from routes import home_route

app.register_blueprint(home_route.bp)

# 이 조건을 달지 않으면, css같은 사항 변화를 12시간마다 체크한다. 즉 디버깅모드에서는 불편하므로, 디버깅시에는 1초로 변경하는 것.
if app.config['DEBUG']:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


# 홈 화면 주기
@app.route('/')
def home():
    modified_all_articles = []
    all_articles = list(db.articles.find({}, {}).sort('like', pymongo.DESCENDING))

    for article in all_articles:
        id = article['_id']

        # 글쓴이의 이미지를 userDb에서 가져오기
        writer_id = article['writer_id']
        writer_img = db.users.find_one({'user_id':writer_id},{})['user_img']
        article['writer_img'] = writer_img

        comments = list(db.comments.find({'article_id':id},{}).sort('post_date', pymongo.DESCENDING))
        if len(comments) !=0:
            comment1 = comments[0]['contents']
            commenter1_id = comments[0]['commenter_id']
            commenter1_img = db.users.find_one({'user_id':commenter1_id},{})['user_img']
            article['commenter1_img'] = commenter1_img
            if len(comments) >= 2:
                comment2 = comments[1]['contents']
                commenter2_id = comments[1]['commenter_id']
                commenter2_img = db.users.find_one({'user_id': commenter2_id}, {})['user_img']
                article['commenter2_img'] = commenter2_img
            else:
                comment2 = ""
        else:
            comment1 = ""
            comment2 = ""

        article['comment1'] = comment1
        article['comment2'] = comment2
        modified_all_articles.append(article)

    return render_template('index.html', results=modified_all_articles)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
