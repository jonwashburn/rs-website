#!/usr/bin/env python3
"""
Quick test of the Astrology OS API functions
"""

import datetime as _dt
from astrology_os import window_score, state_vector, zodiac_hash, global_cost, generate_heatmap

def test_api_functions():
    print("🌟 Testing Astrology OS Core Functions...")
    
    # Test window score
    test_time = _dt.datetime(2025, 1, 15, 12, 0, 0)
    vec = state_vector(test_time)
    score = window_score(test_time)
    zhash = zodiac_hash(vec)
    cost = global_cost(vec)
    
    print(f"✅ Window Score: {score:.6f}")
    print(f"✅ Zodiac Hash: {zhash}")
    print(f"✅ Global Cost: {cost:.6f}")
    
    # Test API-style response
    response = {
        "timestamp": "2025-01-15T12:00:00",
        "window_score": score,
        "zodiac_hash": zhash,
        "global_cost": cost,
        "framework": "Recognition Science"
    }
    
    print("\n📡 API Response Format:")
    import json
    print(json.dumps(response, indent=2))
    
    print("\n🔥 All API functions working! Ready for web deployment.")

if __name__ == "__main__":
    test_api_functions()