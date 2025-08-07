#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime as _dt
from astrology_os import window_score, state_vector, zodiac_hash, global_cost, generate_heatmap

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/window_score')
def get_window_score():
    ts_str = request.args.get('timestamp')
    try:
        ts = _dt.datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        vec = state_vector(ts)
        return jsonify({"timestamp": ts_str, "window_score": window_score(ts), "zodiac_hash": zodiac_hash(vec), "global_cost": global_cost(vec)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/heatmap')
def get_heatmap():
    year_str = request.args.get('year')
    try:
        return jsonify(generate_heatmap(int(year_str)))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)