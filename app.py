import uuid
from datetime import datetime

import pymongo
from flask import Flask, render_template, request, redirect, jsonify
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


#  광훈님 api
# 카드 클릭 시 단일 게시물 보여주기
# 댓글작성 (POST) API
@app.route('/api/single/post_comment', methods=['POST'])
def post_comment():
    comment_receive = request.form['comment_give']
    today_receive = request.form['date_give']
    userId_receive = request.form['userID_give']
# 유저의 아이디와 이름을 어떻게 가져와야 할지 몰라서 doc에 유저이름이 없습니다! - 연습하고 있는거에는 id를 던지고 있는데 해당 프로젝트에서는 아직 안되서...
    doc = {
        'contents': comment_receive,
        'post_date': today_receive,
        'commenter_id': userId_receive
    }
    db.comments.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '저장 완료!'})


# 카드 클릭 시 단일 게시물 보여주기

# 댓글리스트로 보여주기
@app.route('/memo', methods=['GET'])
def listing():
    comments = list(db.prac12.find({},{'_id':False}))
    print(comments)
    return jsonify({'all_comments':comments})


# 유저체크하기
@app.route('/api/single/check_user', methods=['GET'])
def checkUser():

    user = db.users.find_one({'name': 'bobby'})

    title_receive = request.form['title_give']
    db.prac12.update_one({'title': title_receive})

    # db.users.update_one({'name': 'bobby'}, {'$set': {'age': 19}})

    return jsonify({'msg': '수정완료!'})

# 댓글수정
@app.route('/api/single/update_comment', methods=['POST'])
def update_comment():

    title_receive = request.form['title_give']
    db.prac12.update_one({'title': title_receive})

    # db.users.update_one({'name': 'bobby'}, {'$set': {'age': 19}})

    return jsonify({'msg': '수정완료!'})

# 댓글삭제
@app.route('/api/single/delete_comment', methods=['POST'])
def delete_comment():
    title_receive = request.form['title_give']
    db.prac12.delete_one({'title': title_receive})

    return jsonify({'msg': '삭제완료!'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
