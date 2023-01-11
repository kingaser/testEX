from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.9wvifvb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    movie_list = list(db.movies.find({}, {'_id': False}))
    cnt = len(movie_list) + 1

    doc = {
        'star': star_receive,
        'comment': comment_receive,
        'title':title,
        'image':image,
        'desc':desc,
        'num':cnt
    }

    db.movies.insert_one(doc)

    return jsonify({'msg':'등록 완료!'})

@app.route("/movie/remove", methods=["POST"])
def movie_remove():
    num_receive = request.form['num_give']
    db.movies.delete_one({'num': int(num_receive)})
    return jsonify(({'msg':'기록 삭제!'}))

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies':movie_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)