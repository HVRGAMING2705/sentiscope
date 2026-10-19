"""SentiScope — sentiment analyzer for product reviews.
Trains TF-IDF + Logistic Regression on a built-in labeled dataset and
exports the model weights (idf + coefficients) as JSON so the same math
runs in the browser demo with no backend.
"""
import json
import math
import random

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ---- Synthetic dataset generation (class-controlled templates) ----
POS_NOUNS = ["phone", "headphones", "laptop", "camera", "speaker", "keyboard",
             "smartwatch", "tablet", "earbuds", "monitor", "charger", "mouse",
             "gadget", "device", "product", "item", "purchase", "order"]
POS_ADJ = ["amazing", "excellent", "fantastic", "wonderful", "outstanding",
           "superb", "perfect", "awesome", "brilliant", "incredible",
           "great", "lovely", "impressive", "stunning", "reliable"]
POS_TPL = [
    "I love this {n}, it is {a} and works perfectly",
    "This {n} is {a}, I am very happy with my purchase",
    "The {n} has {a} quality, highly recommended",
    "What an {a} {n}, exceeded all my expectations",
    "My new {n} is {a}, best money I ever spent",
    "Really {a} {n}, setup was quick and painless",
    "The {n} feels {a}, solid build and great finish",
    "An {a} {n} for the price, I tell everyone to buy it",
    "This {n} is {a}, battery lasts all day long",
    "Absolutely {a} {n}, five stars from me",
    "The {n} is {a} and arrived earlier than expected",
    "So pleased with this {a} {n}, works like a charm",
]
NEG_ADJ = ["terrible", "awful", "horrible", "poor", "disappointing", "cheap",
           "flimsy", "useless", "mediocre", "faulty", "bad", "unreliable",
           "shoddy", "broken", "dreadful"]
NEG_TPL = [
    "I hate this {n}, it is {a} and a waste of money",
    "This {n} is {a}, I regret buying it completely",
    "The {n} has {a} quality, do not recommend it",
    "What an {a} {n}, stopped working within days",
    "My new {n} is {a}, worst purchase ever",
    "Really {a} {n}, it broke after one week",
    "The {n} feels {a}, flimsy and cheap plastic",
    "An {a} {n} for the price, avoid it at all costs",
    "This {n} is {a}, battery drains in an hour",
    "Absolutely {a} {n}, I returned it the same day",
    "The {n} is {a} and arrived damaged in the box",
    "So disappointed with this {a} {n}, total garbage",
]

rng = random.Random(42)
POS = [t.format(n=rng.choice(POS_NOUNS), a=rng.choice(POS_ADJ)) for t in POS_TPL for _ in range(9)]
NEG = [t.format(n=rng.choice(POS_NOUNS), a=rng.choice(NEG_ADJ)) for t in NEG_TPL for _ in range(9)]
rng.shuffle(POS); rng.shuffle(NEG)
texts = POS + NEG
labels = [1] * len(POS) + [0] * len(NEG)

random.seed(42)
np.random.seed(42)

# Stratified 5-fold cross-validation on the whole dataset (honest metric on
# small data), then train the final model on ALL data for the exported weights.
X = np.array(texts)
y = np.array(labels)
from sklearn.model_selection import StratifiedKFold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fold_accs = []
for tri, tei in skf.split(X, y):
    v = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 1), max_features=150, sublinear_tf=True
    )
    Xtr = v.fit_transform(X[tri])
    Xte = v.transform(X[tei])
    c = LogisticRegression(C=0.5, max_iter=1000, random_state=42)
    c.fit(Xtr, y[tri])
    fold_accs.append(accuracy_score(y[tei], c.predict(Xte)))
acc = float(np.mean(fold_accs))
print(f"5-fold CV accuracy: {acc:.3f} (folds={['%.2f' % a for a in fold_accs]})")

vectorizer = TfidfVectorizer(
    stop_words="english", ngram_range=(1, 1), max_features=150, sublinear_tf=True
)
Xtr = vectorizer.fit_transform(texts)

clf = LogisticRegression(C=0.5, max_iter=1000, random_state=42)
clf.fit(Xtr, y)
print(f"trained on {Xtr.shape[0]} samples, {Xtr.shape[1]} features")

feature_names = vectorizer.get_feature_names_out()
coef = clf.coef_[0]
idf = vectorizer.idf_

from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

weights = {
    "vocab": feature_names.tolist(),
    "idf": [round(float(v), 4) for v in idf],
    "coef": [round(float(v), 4) for v in coef],
    "intercept": round(float(clf.intercept_[0]), 4),
    "accuracy": round(float(acc), 4),
    "stop_words": sorted(ENGLISH_STOP_WORDS),
}

with open("weights.json", "w") as f:
    json.dump(weights, f)

print(f"exported weights.json ({len(feature_names)} features)")

# Show most positive / negative words as a sanity check
order = np.argsort(coef)
print("most negative:", [feature_names[i] for i in order[:8]])
print("most positive:", [feature_names[i] for i in order[-8:][::-1]])
