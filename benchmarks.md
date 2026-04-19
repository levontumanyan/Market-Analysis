# Market Analysis Benchmarks

This document explains the scoring logic and benchmark configuration used to evaluate company fundamentals.

# Insider Ownership (`heldPercentInsiders`)

Insider ownership is a critical fundamental metric that represents the percentage of a company's stock owned by its management, directors, and other key individuals within the company.

## Why use a Bell Curve?

A **Bell Curve** (Gaussian distribution) is used for this metric because insider ownership is a "goldilocks" indicator. A simple linear or sigmoid (monotonic) scale—where more is always better—fails to capture the risks associated with extremely high ownership levels.

- **Low Ownership (< 5%)**: Management has little "skin in the game." This can lead to a lack of alignment between management and shareholders, as executives may not be personally invested in the long-term stock performance.
- **Optimal Range (10-25%)**: This is the "sweet spot." It demonstrates that management has significant personal wealth tied to the company's success, which strongly aligns their interests with those of public shareholders.
- **High/Extreme Ownership (> 50%)**: While management is highly aligned, this creates "control risk" or "entrenchment." Insiders can make decisions without needing to consider minority shareholders, and the stock often suffers from low liquidity (fewer shares available for the public to trade).

## Scoring Logic

The scoring function uses a Gaussian curve centered on a target value:

$$ \text{Score} = e^{-0.5 \cdot \left(\frac{\text{val} - \text{target}}{\text{width}}\right)^2} $$

### Parameters:
- **Target (`0.15`)**: A 15% ownership level is considered the ideal balance between alignment and control.
- **Width (`0.10`)**: This parameter determines how quickly the score decays as the value moves away from the target.

### Resulting Scores:
- **15% (Target)**: **1.00 (100%)** - Perfect alignment.
- **10% or 20%**: **~0.88 (88%)** - Very strong signal.
- **5% or 25%**: **~0.60 (60%)** - Good, but getting less ideal.
- **0%**: **~0.32 (32%)** - No skin in the game.
- **50%**: **~0.002 (0.2%)** - Significant control/liquidity risk.

By using this approach, we prioritize companies with healthy, balanced insider alignment while flagging those with either insufficient commitment or excessive control.
