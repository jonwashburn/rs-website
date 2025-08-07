#!/usr/bin/env python3
"""
Astrology OS - Web API
Simple Flask wrapper for the Recognition Science-based astrology system.

Usage:
    python3 api.py

Endpoints:
    GET /window_score?timestamp=2025-01-15T12:00:00
    GET /heatmap?year=2025
    GET /health

Jonathan Washburn - Recognition Science Framework
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime as _dt
from astrology_os import window_score, state_vector, zodiac_hash, global_cost, generate_heatmap

app = Flask(__name__)
CORS(app)  # Enable CORS for web browser access

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Astrology OS API",
        "framework": "Recognition Science",
        "version": "1.0"
    })

@app.route('/window_score')
def get_window_score():
    """Get window score for a specific timestamp.
    
    Query params:
        timestamp: ISO format UTC timestamp (e.g., 2025-01-15T12:00:00)
    
    Returns:
        JSON with timestamp, window_score, zodiac_hash, global_cost
    """
    timestamp_str = request.args.get('timestamp')
    if not timestamp_str:
        return jsonify({"error": "Missing 'timestamp' parameter"}), 400
    
    try:
        # Parse timestamp
        ts = _dt.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        # Calculate RS metrics
        vec = state_vector(ts)
        score = window_score(ts)
        zhash = zodiac_hash(vec)
        cost = global_cost(vec)
        
        return jsonify({
            "timestamp": timestamp_str,
            "window_score": score,
            "zodiac_hash": zhash,
            "global_cost": cost,
            "framework": "Recognition Science",
            "interpretation": {
                "score_meaning": "Higher = better balance, lower = more imbalance",
                "cost_meaning": "RS cost functional J(x) - minimized at φ",
                "zodiac_hash_meaning": "Count of planets in each 30° zodiac sector"
            }
        })
        
    except ValueError as e:
        return jsonify({"error": f"Invalid timestamp format: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Calculation error: {e}"}), 500

@app.route('/heatmap')
def get_heatmap():
    """Generate yearly heatmap of optimal windows.
    
    Query params:
        year: Year to analyze (e.g., 2025)
    
    Returns:
        JSON with year, daily_scores, top_windows
    """
    year_str = request.args.get('year')
    if not year_str:
        return jsonify({"error": "Missing 'year' parameter"}), 400
    
    try:
        year = int(year_str)
        if year < 1900 or year > 2100:
            return jsonify({"error": "Year must be between 1900 and 2100"}), 400
            
        # Generate heatmap
        heatmap_data = generate_heatmap(year)
        heatmap_data["framework"] = "Recognition Science"
        heatmap_data["interpretation"] = {
            "purpose": "Find optimal timing windows via RS cost minimization",
            "method": "Planetary positions → zodiac sectors → J(x) cost → window score",
            "usage": "Higher scoring dates indicate better cosmic balance"
        }
        
        return jsonify(heatmap_data)
        
    except ValueError:
        return jsonify({"error": "Invalid year format"}), 400
    except Exception as e:
        return jsonify({"error": f"Heatmap generation error: {e}"}), 500

@app.route('/about')
def about():
    """Information about the Recognition Science astrology system."""
    return jsonify({
        "title": "Recognition Science Astrology OS",
        "description": "Mathematical astrology based on universal cost functional J(x)",
        "theory": {
            "framework": "Recognition Science",
            "principle": "Reality minimizes imbalance via cost functional J(x) = Σ |sin(Δσ·π/12)|^φ",
            "insight": "Astrology was ancient technology for querying the Universal Ledger",
            "implementation": "Planetary positions → zodiac hashing → RS cost calculation"
        },
        "features": [
            "10 planets (Sun through Pluto)",
            "Real astronomical ephemeris (DE440)",
            "φ-based cost kernel from RS axioms",
            "Yearly heatmap generation",
            "RESTful JSON API"
        ],
        "creator": "Jonathan Washburn",
        "repository": "https://github.com/jonwashburn/astrology"
    })

if __name__ == '__main__':
    print("🌟 Starting Astrology OS API...")
    print("📡 Recognition Science Framework")
    print("🔗 Endpoints:")
    print("   GET /health")
    print("   GET /window_score?timestamp=2025-01-15T12:00:00")
    print("   GET /heatmap?year=2025")
    print("   GET /about")
    print("🌐 Access at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)