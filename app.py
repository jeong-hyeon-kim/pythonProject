import uuid
from datetime import datetime

import pymongo
from flask import Flask, render_template, request, redirect

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
        comments = list(db.comments.find({'article_id':id},{}).sort('post_date', pymongo.DESCENDING))
        if len(comments) !=0:
            comment1 = comments[0]['contents']
            if len(comments) >= 2:
                comment2 = comments[1]['contents']
            else:
                comment2 = ""
        else:
            comment1 = ""
            comment2 = ""
        article['comment1'] = comment1
        article['comment2'] = comment2
        modified_all_articles.append(article)

    return render_template('index.html', results=modified_all_articles)


# comment(댓글) 더미데이터 넣어보기
# time_now = datetime.now()
# now_text = time_now.strftime("%Y{} %m{} %d{} %H{} %M{}")
# now_text = now_text.format('년', '월', '일', '시', '분')
#
# comment_li = []
# comment1 = {
#     "_id": uuid.uuid4().hex,
#     "commenter_id": "id01",
#     "commenter_name": "여름스누피",
#     "article_id": "9198a343f03642eda96035e754972ff4", # 폐허의 아이디.
#     "contents": "완전 좋아요!(댓글가져오기)",
#     "post_date": now_text
#     # 코멘터의 이미지도 넣어놓는게 좋을까? 아니면 불러올 때 유저테이블에서?
# }
# comment2 = {
#     "_id": uuid.uuid4().hex,
#     "commenter_id": "id02",
#     "commenter_name": "가을스누피",
#     "article_id": "9198a343f03642eda96035e754972ff4", # 폐허의 아이디.
#     "contents": "완전 좋아요22(댓글가져오기)",
#     "post_date": now_text
#     # 코멘터의 이미지도 넣어놓는게 좋을까? 아니면 불러올 때 유저테이블에서?
# }
#
# comment_li.append(comment1)
# comment_li.append(comment2)
#
# db.comments.insert_many(comment_li)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
