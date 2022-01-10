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
    found_articles = list(db.articles.find({'$or': [{'album_singer':{'$regex': keyword}}, {'album_title':{'$regex': keyword}}]},{}))
    return jsonify({'found_articles': found_articles})
    # return render_template('templates/index.html', results = found_articles)

# 좋아요
