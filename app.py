from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import time

app = Flask(__name__)

# Simple in-memory cache for trend data
trend_cache = {}

@app.route('/', methods=['GET'])
def home():
    return "✅ PyTrends API is live. Use /trends?keyword=your_keyword"

@app.route('/trends', methods=['GET'])
def get_trends():
    keyword = request.args.get('keyword')

    # Block missing, undefined, or empty keyword inputs
    if not keyword or keyword.strip().lower() in ["undefined", "null", ""]:
        return jsonify({"error": "A valid keyword is required"}), 400

    # Check cache (data is valid for 1 hour)
    cached = trend_cache.get(keyword)
    if cached and time.time() - cached["ts"] < 3600:
        return jsonify({"keyword": keyword, "interest": cached["data"]})

    try:
        # Initialize PyTrends with retries and backoff to handle rate limits
        pytrends = TrendReq(hl='en-US', tz=360, retries=5, backoff_factor=0.1)
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')

        data = pytrends.interest_over_time()
        if data.empty:
            return jsonify({"error": f"No trend data found for '{keyword}'"}), 404

        # Drop NaN and convert pandas timestamps to strings with integer values
        series = data[keyword].dropna()
        response = {k.strftime('%Y-%m-%d'): int(v) for k, v in series.items()}

        # Store in cache
        trend_cache[keyword] = {"ts": time.time(), "data": response}

        return jsonify({"keyword": keyword, "interest": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
