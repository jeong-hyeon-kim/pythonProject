import pymongo
from flask import Flask, render_template,  request, redirect
app = Flask(__name__)

from pymongo import MongoClient

#TODO EC2랑 연결된 mongoDb로 변경
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
    all_articles = list(db.articles.find({}, {}).sort('like', pymongo.DESCENDING))
    return render_template('index.html', results=all_articles)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)