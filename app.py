from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)
pytrends = TrendReq()

@app.route('/trend', methods=['POST'])
def get_trend_score():
    data = request.get_json()
    keyword = data.get('keyword')

    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    try:
        pytrends.build_payload([keyword], timeframe='today 12-m')
        interest = pytrends.interest_over_time()

        if interest.empty:
            return jsonify({"keyword": keyword, "trend_score": 0})

        trend_score = int(interest[keyword].mean())
        return jsonify({"keyword": keyword, "trend_score": trend_score})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
