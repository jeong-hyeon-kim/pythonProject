import flask
from flask import Flask, render_template, jsonify, request, Blueprint
import pymongo
import re

from pymongo import MongoClient

# TODO client를 ec2 host로 변경!
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.mini


NAME = "home"
bp = Blueprint(NAME, __name__, template_folder='templates', url_prefix="/api/home")

# API - home(jinjatry.html)에서 연결된 부분들
@bp.route('/articles')
def all_articles():
    all_articles = list(db.articles.find({}, {}).sort('like', pymongo.DESCENDING))
    return jsonify({'all_articles': all_articles})
    # return render_template('templates/index.html', results = all_articles)


@bp.route('/search_article')
def keyword_search():
    keyword = request.args.get('keyword')
    print(keyword)
    found_articles = list(db.articles.find({'$or': [{'album_singer':{'$regex': keyword}}, {'album_title':{'$regex': keyword}}]},{}))
    return jsonify({'found_articles': found_articles})
    # return render_template('templates/index.html', results = found_articles)