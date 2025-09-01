# app.py
import os
from flask import Flask, request, jsonify
from db import init_db, get_db, insert_feedback, get_stats
from transformers import pipeline

app = Flask(__name__)

# Lazy-load model once per process
MODEL_NAME = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
sentiment_pipe = pipeline("sentiment-analysis", model=MODEL_NAME)

@app.before_first_request
def _init():
    init_db()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/feedback")
def create_feedback():
    data = request.get_json(force=True)
    text = (data or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400

    # Predict sentiment
    pred = sentiment_pipe(text)[0]  # {'label': 'POSITIVE', 'score': 0.999...}
    label = pred["label"].upper()
    score = float(pred["score"])

    db = get_db()
    insert_feedback(db, text, label, score)
    return jsonify({"text": text, "sentiment": label, "score": score})

@app.get("/dashboard")
def dashboard():
    db = get_db()
    stats = get_stats(db)
    return jsonify(stats)

if __name__ == "__main__":
    # Dev server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
