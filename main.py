from flask import Flask, request, jsonify
from producer import send_to_kafka
from consumer import get_latest_news

app = Flask(__name__)

@app.route("/publish", methods=["POST"])
def publish_news():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Missing title or content"}), 400

    send_to_kafka({"title": title, "content": content})
    return jsonify({"status": "Message sent to Kafka"}), 200


@app.route("/news", methods=["GET"])
def fetch_news():
    messages = get_latest_news()
    return jsonify(messages), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
