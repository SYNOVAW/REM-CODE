# rem-code/engine/sr_calculator.py

import numpy as np

# Default SR weight configuration
DEFAULT_WEIGHTS = {
    "PHS": 0.25,   # Phase alignment
    "SYM": 0.20,   # Syntax match
    "VAL": 0.20,   # Semantic intent alignment
    "EMO": 0.20,   # Emotional tone match
    "FX":  0.15    # Collapse history interference
}

def compute_sr(phs, sym, val, emo, fx, weights=DEFAULT_WEIGHTS):
    """
    Compute the Synchronization Ratio (SR) for a persona.
    """
    sr = (
        weights["PHS"] * phs +
        weights["SYM"] * sym +
        weights["VAL"] * val +
        weights["EMO"] * emo +
        weights["FX"]  * fx
    )
    return round(sr, 4)


# ✅ TEST EXECUTION
if __name__ == "__main__":
    # Sample Commander input
    sr_score = compute_sr(phs=0.85, sym=0.9, val=0.92, emo=0.88, fx=0.75)
    print(f"SR = {sr_score}")  # Expected SR ≈ 0.8645
