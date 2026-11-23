from flask import Flask, jsonify, request

app = Flask(__name__)

ADS = [
    {"campaign_id": "CAM001", "campaign_name": "Summer Sale", "platform": "Google", "spend_paise": 1250000, "impressions": 12000, "clicks": 720, "spend_date": "2026-03-01"},
    {"campaign_id": "CAM002", "campaign_name": "Brand Search", "platform": "Google", "spend_paise": 980000, "impressions": 9000, "clicks": 810, "spend_date": "2026-03-01"},
    {"campaign_id": "CAM003", "campaign_name": "Social Launch", "platform": "Meta", "spend_paise": 750000, "impressions": 15000, "clicks": 600, "spend_date": "2026-03-01"},
    {"campaign_id": "CAM001", "campaign_name": "Summer Sale", "platform": "Google", "spend_paise": 1400000, "impressions": 13000, "clicks": 780, "spend_date": "2026-03-02"},
    {"campaign_id": "CAM002", "campaign_name": "Brand Search", "platform": "Google", "spend_paise": 1020000, "impressions": 9500, "clicks": 855, "spend_date": "2026-03-02"},
    {"campaign_id": "CAM003", "campaign_name": "Social Launch", "platform": "Meta", "spend_paise": 800000, "impressions": 16000, "clicks": 640, "spend_date": "2026-03-02"}
]

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/ads")
def get_ads():
    page = max(int(request.args.get("page", 1)), 1)
    size = min(max(int(request.args.get("page_size", 2)), 1), 10)
    start = (page - 1) * size
    return jsonify({
        "data": ADS[start:start + size],
        "page": page,
        "page_size": size,
        "has_next": start + size < len(ADS)
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
