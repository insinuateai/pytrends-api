from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

# ✅ New root route for UX
@app.route('/')
def home():
    return "✅ PyTrends API is live. Use /trends?keyword=your_keyword"

@app.route('/trends', methods=['GET'])
def get_trends():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')

    data = pytrends.interest_over_time()
    if data.empty:
        return jsonify({"error": "No trend data found for keyword"}), 404

    response = data[keyword].dropna().to_dict()
    return jsonify({"keyword": keyword, "interest": response})
