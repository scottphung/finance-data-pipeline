# 🧠 Engineering Notes — Quant Hedge Fund System

This document explains the design decisions, bugs encountered, and how they were solved.

---

# 1. 🏗 System Design Decisions

## Why FastAPI + Streamlit?

- FastAPI → fast, async, production-style API layer
- Streamlit → rapid visualization for financial dashboards

Separation allows:
- backend reuse (APIs)
- frontend flexibility

---

# 2. ⚠️ Major Problems Encountered

## ❌ Problem 1: Missing or inconsistent Yahoo Finance data

### Issue:
Different tickers returned different schema formats.

### Fix:
- Normalized columns
- Implemented dynamic column detection
```python
if "close" in df.columns: