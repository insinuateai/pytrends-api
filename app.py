from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)
pytrends = TrendReq()

@app.route("/", methods=["POST"])
def google_trends():
    data = request.get_json()
    keyword = data.get("keyword")

    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    pytrends.build_payload([keyword], timeframe='today 12-m')
    interest = pytrends.interest_over_time()

    if interest.empty:
        return jsonify({"error": "No trend data found"}), 404

    trend_score = int(interest[keyword].iloc[-1])
    return jsonify({"keyword": keyword, "trend_score": trend_score})
