import flask
from flask import Flask, render_template, jsonify, request, Blueprint
import re
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.mini

NAME = "home"
bp = Blueprint(NAME, __name__, template_folder='templates', url_prefix="/api/home")

# API

# 검색
@bp.route('/search_article')
def keyword_search():
    keyword = request.args.get('keyword')
    print(keyword)
    modified_all_articles = []

    found_articles = list(db.articles.find({'$or': [{'album_singer':{'$regex': keyword}}, {'album_title':{'$regex': keyword}}]},{}))
    for article in found_articles:
        id = article['_id']

        comments = list(db.comments.find({'article_id': id}, {}).sort('post_date', pymongo.DESCENDING))
        if len(comments) != 0:
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
    # comments = db.comments.find({'article_id':})
    return jsonify({'found_articles': modified_all_articles})
    # return render_template('templates/index.html', results = found_articles)

# 좋아요
@bp.route('/like', methods=['POST'])
def like():
    # like_num = request.form['like']
    article_id = request.form['article_id']
    print(article_id)

    target_like = db.articles.find_one({'_id':article_id}, {})['like']
    print(target_like)
    target_like += 1
    db.articles.update_one({'_id':article_id}, {'$set': {'like': target_like}})
    return jsonify({'message': '좋아요 완료!'})