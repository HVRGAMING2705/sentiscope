# SentiScope 🔍

ML-powered **sentiment analyzer for product reviews** — type any review and a real trained model scores it positive or negative, right in the browser.

**Live demo:** https://sentiscope.vercel.app

## How it works

1. **Data** — 216 labeled product reviews (positive / negative) generated from sentiment-controlled templates in `train.py`.
2. **Features** — TF-IDF unigrams (sublinear TF, L2-normalized) via scikit-learn.
3. **Model** — Logistic regression. **5-fold cross-validation accuracy: 100%.**
4. **Browser demo** — `train.py` exports the vocabulary, idf values, coefficients, intercept, and stop-word list to `weights.json`. The site's JavaScript re-runs the exact same math as sklearn (`σ(w·x + b)` with L2-normalized TF-IDF) — verified to match Python's predictions to 4 decimals. No backend, no API calls.

## Reproduce

```bash
pip install scikit-learn numpy
python train.py   # retrains and regenerates weights.json
```

## Files

- `train.py` — dataset generation, training, evaluation, weight export
- `weights.json` — exported model (107 features)
- `index.html` — the interactive demo site
- `vercel.json` — static hosting config + security headers

Built by [Vikranth Reddy](https://github.com/HVRGAMING2705) · B.Tech CSE (AI & ML), Woxsen University
