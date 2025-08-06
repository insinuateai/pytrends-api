from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "\u2705 PyTrends API is live. Use /trends?keyword=your_keyword"

@app.route('/trends', methods=['GET'])
def get_trends():
    keyword = request.args.get('keyword')

    # Block missing, undefined, or empty keyword inputs
    if not keyword or keyword.strip().lower() in ["undefined", "null", ""]:
        return jsonify({"error": "A valid keyword is required"}), 400

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')

        data = pytrends.interest_over_time()
        if data.empty:
            return jsonify({"error": f"No trend data found for '{keyword}'"}), 404

        response = data[keyword].dropna().to_dict()
        return jsonify({"keyword": keyword, "interest": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
