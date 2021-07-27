import os
import requests
import engine
from flask import Flask,render_template,request,jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Tour bot peer recommendation system online !"


@app.route('/recommendpeer')
def recommend_peer():
    user = request.args.get("uname")
    results = engine.recommend(user)
    return jsonify(results)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False,host='0.0.0.0', port=port)