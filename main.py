import os
from flask import Flask, request, jsonify
import snscrape.modules.twitter as sntwitter

app = Flask(__name__)
SECRET_API_KEY = os.getenv('API_KEY')

@app.before_request
def check_api_key():
    if request.path == '/search':
        provided_key = request.headers.get('Authorization')
        if not provided_key or not provided_key.startswith('Bearer '):
            return jsonify({"error": "Authorization header is missing or invalid."}), 401
        
        provided_key = provided_key.split(' ')[1]
        if provided_key != SECRET_API_KEY:
            return jsonify({"error": "Invalid API Key"}), 403

@app.route('/search', methods=['GET'])
def search_tweets():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "検索キーワード 'query' を指定してください。"}), 400

    tweets = []
    limit = 10
    try:
        scraper = sntwitter.TwitterSearchScraper(f"{query} lang:ja")
        for i, tweet in enumerate(scraper.get_items()):
            if i >= limit:
                break
            tweets.append({
                "date": tweet.date.isoformat(),
                "user": tweet.user.username,
                "content": tweet.rawContent
            })
        return jsonify(tweets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
