"""Builds the SentiScope project presentation (9 slides)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

INK = RGBColor(0x11, 0x11, 0x11)
ACCENT = RGBColor(0x0A, 0x7A, 0x2F)
GREY = RGBColor(0x55, 0x55, 0x55)
LIGHT = RGBColor(0xFA, 0xFA, 0xFA)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

def add_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    bg.line.fill.background()

def title_slide(text, sub=None, accent=False):
    s = prs.slides.add_slide(blank); add_bg(s)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(0.12), Inches(4.6))
    bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT if accent else INK
    bar.line.fill.background()
    tx = s.shapes.add_textbox(Inches(1.3), Inches(1.5), Inches(10.5), Inches(2.2))
    p = tx.text_frame.paragraphs[0]; p.text = text
    p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = INK
    if sub:
        tx2 = s.shapes.add_textbox(Inches(1.3), Inches(3.9), Inches(10.5), Inches(2.5))
        for i, line in enumerate(sub):
            p = tx2.text_frame.add_paragraph() if i else tx2.text_frame.paragraphs[0]
            p.text = line; p.font.size = Pt(20); p.font.color.rgb = GREY; p.space_after = Pt(8)
    return s

def bullet_slide(title, bullets, number):
    s = prs.slides.add_slide(blank); add_bg(s)
    tag = s.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(2), Inches(0.6))
    p = tag.text_frame.paragraphs[0]; p.text = f"{number:02d}"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = ACCENT
    th = s.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.7), Inches(1.1))
    p = th.text_frame.paragraphs[0]; p.text = title
    p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = INK
    tb = s.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(11.7), Inches(4.6))
    tf = tb.text_frame; tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.add_paragraph() if i else tf.paragraphs[0]
        p.text = "•  " + b; p.font.size = Pt(20); p.font.color.rgb = INK
        p.space_after = Pt(14); p.level = 0
    return s

# 1 — Title
title_slide("SentiScope", [
    "AI-Powered Sentiment Analyzer for Product Reviews",
    "",
    "Vikranth Reddy  |  B.Tech CSE (AI & ML), Woxsen University",
    "Daily AI/ML Project Factory — Day 2  ·  19 October 2026",
], accent=True)

# 2 — Problem
bullet_slide("The Problem", [
    "E-commerce sites get thousands of product reviews every day — no human can read them all.",
    "Sellers need a fast, automatic way to know whether customers are happy or angry.",
    "Manual star-ratings are noisy: people write glowing text with 1 star, and vice versa.",
    "Goal: type a review → get an instant positive/negative verdict from a real ML model.",
], 2)

# 3 — Solution
bullet_slide("The Solution", [
    "SentiScope: a sentiment analyzer trained on 216 labeled product reviews.",
    "Pipeline: text → TF-IDF word features → logistic regression → probability of “positive”.",
    "The trained weights are exported to weights.json — the website re-runs the exact same math in JavaScript.",
    "Zero backend: the whole model lives in the browser. Verified to match Python's predictions exactly.",
], 3)

# 4 — Tech Stack
bullet_slide("Tech Stack", [
    "Python, scikit-learn, NumPy — training & evaluation (train.py).",
    "TF-IDF vectorizer: unigrams, English stop-words removed, sublinear TF, L2 normalization.",
    "Logistic regression classifier (C = 0.5).",
    "Vanilla JavaScript — in-browser inference, no frameworks.",
    "Static hosting on Vercel with hardened security headers.",
], 4)

# 5 — Architecture
bullet_slide("Architecture", [
    "train.py:  (1) generate 216 reviews from sentiment-controlled templates → (2) split 5-fold → (3) TF-IDF fit → (4) logistic regression → (5) export weights.json.",
    "weights.json: vocabulary (107 words), idf values, coefficients, intercept, stop-word list — 12 KB.",
    "index.html: tokenizer (sklearn-compatible) → TF-IDF → σ(w·x + b) → probability bar + top contributing words.",
    "Same input in Python and JS gives the same probability — parity checked to 4 decimals.",
], 5)

# 6 — Demo
bullet_slide("Live Demo", [
    "Try: “I love this phone, the camera is amazing” → 😊 Positive, P ≈ 0.65.",
    "Try: “Terrible product, it broke after two days” → 😞 Negative, P ≈ 0.23.",
    "The demo also shows which words pushed the decision (e.g. amazing +0.31, terrible −0.42).",
    "Demo URL: sentiscope.vercel.app",
], 6)

# 7 — Results
bullet_slide("Results", [
    "5-fold cross-validation accuracy: 100% (216 reviews, stratified folds).",
    "Most positive words learned: great, works, wonderful, exceeded, expectations.",
    "Most negative words learned: poor, flimsy, terrible, awful, cheap.",
    "Known limitation: negation (“not bad”) is misclassified — unigram models can't see word order.",
], 7)

# 8 — Future Scope
bullet_slide("Future Scope", [
    "Handle negation and bigrams (“not good”, “very bad”) for harder reviews.",
    "Train on a real public dataset (e.g. 50k IMDB movie reviews).",
    "Try stronger models: Naive Bayes baseline, then a small transformer (DistilBERT).",
    "Add a third class: neutral / mixed sentiment.",
    "Multi-language reviews (Telugu + English code-mix).",
], 8)

# 9 — Thank you
s = prs.slides.add_slide(blank); add_bg(s)
tx = s.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(2))
p = tx.text_frame.paragraphs[0]; p.text = "Thank You"
p.font.size = Pt(60); p.font.bold = True; p.font.color.rgb = INK; p.alignment = PP_ALIGN.CENTER
tx2 = s.shapes.add_textbox(Inches(1.5), Inches(4.2), Inches(10.3), Inches(1.5))
p = tx2.text_frame.paragraphs[0]
p.text = "GitHub: github.com/HVRGAMING2705/sentiscope\nDemo: sentiscope.vercel.app"
p.font.size = Pt(22); p.font.color.rgb = GREY; p.alignment = PP_ALIGN.CENTER

out = "/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_SentiScope_2026-10-19.pptx"
prs.save(out)
print("saved", out)
