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

# PEG Ratio (`pegRatio`)

The PEG (Price/Earnings-to-Growth) Ratio is a key metric that balances valuation (P/E) with earnings growth.

## Why use a Bell Curve?

Initially, a **Sigmoid Curve** was used to score the PEG ratio. However, we've transitioned to a **Bell Curve** (Gaussian distribution) to better capture the risks associated with extreme valuation outliers.

- **Suspiciously Low (< 0.3)**: A very low PEG ratio (e.g., 0.1) can be a "value trap." It often indicates that the market expects a company's recent high growth to be unsustainable, or it may be due to a one-time earnings spike.
- **Optimal Range (0.5 – 1.0)**: This is the "sweet spot" for growth-at-a-reasonable-price (GARP) investors. A PEG of around 0.7 is often considered the ideal balance of growth and valuation.
- **High/Overvalued (> 2.0)**: A high PEG ratio suggests you are paying significantly more for each unit of growth, indicating potential overvaluation.

## Scoring Logic

The scoring function uses a Gaussian curve centered on a target value:

$$ \text{Score} = e^{-0.5 \cdot \left(\frac{\text{val} - \text{target}}{\text{width}}\right)^2} $$

### Parameters:
- **Target (`0.7`)**: A 0.7 PEG ratio is our "ideal" target for growth value.
- **Width (`0.6`)**: This determines how quickly the score drops off as the ratio moves away from the ideal 0.7 mark.

### Resulting Scores:

| PEG Value | Bell Curve Score | Interpretation |
| :--- | :--- | :--- |
| **0.1** | **~61%** | Suspiciously Low (Caution/Value Trap) |
| **0.4** | **~88%** | Excellent Value |
| **0.7** | **100%** | The "Sweet Spot" (Ideal) |
| **1.0** | **~88%** | Fair Value (Good) |
| **1.5** | **~41%** | Slightly Expensive (Weak) |
| **2.5** | **~1%** | Overvalued (Fail) |

---
**Verdict:** By using a Bell Curve, we prioritize stocks in the healthy "GARP" range while assigning lower scores to extreme outliers that may represent data errors or unsustainable business models.
