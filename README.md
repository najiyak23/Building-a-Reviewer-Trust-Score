# 🏆Building-a-Reviewer-Trust-Score
## 📌 Overview

In today’s digital world, customer reviews play a huge role in how people discover and decide on products. But not all reviews are created equal — some are spammy, biased, or low-effort, while others are authentic, detailed, and genuinely helpful.
This project demonstrates how to build a Reviewer Trust Score, a data-driven metric that ranks reviewers based on the credibility and usefulness of their contributions.

The approach is general, and can be applied to any review platform — from e-commerce apps to brand discovery sites.
## 🛑 The Problem
- Many platforms treat all reviews the same.
- This makes it hard for users to know which reviews to trust.
- Low-quality reviews can reduce confidence in the platform and hurt user experience.

## ✅ The Solution

I design a Trust Score (scaled 0–1) that measures the trustworthiness of each reviewer.
The score combines several signals:

1. Activity – How many reviews they’ve written.
2. Consistency – Whether they give balanced ratings (not always 5 stars or always 1 star).
3. Quality – Length of their reviews (more effort suggests higher quality).
4. Community validation – Number of “helpful” votes their reviews receive.
5. Authenticity – Ratio of verified purchases to total reviews.
6. Recency – Whether they are still active.
7. Each factor is normalized and then weighted to create a single interpretable metric.

## 📊 Methodology

### 1. Data Cleaning & Feature Engineering
  - Extracted reviewer-level statistics from raw review data.
  - Created features like num_reviews, avg_helpful_votes, verified_ratio, recent_reviews.
### 2. Normalization
  - Applied Min-Max scaling to bring all features onto a 0–1 scale.
  - Prevents large numbers (like votes) from dominating small numbers (like ratios).
### 3. Trust Score Formula
  - Weighted combination of features:
      - Activity (20%)
      - Balance of ratings (15%)
      - Review length (10%)
      - Helpful votes (25%)
      - Verified purchases (15%)
      - Recency (15%)
### 4. Leaderboard
  - Ranked reviewers by trust score to identify the most credible contributors.
## 📈 Results
### 🔝 Top Reviewers Leaderboard
A ranked list of reviewers who consistently provide authentic and helpful reviews.

<img width="886" height="547" alt="image" src="https://github.com/user-attachments/assets/6e37573a-1f02-41c6-a526-6b7ccaf7cd35" />

## 📉 Distribution of Trust Scores
Most reviewers score in the mid-range, with only a small fraction qualifying as highly trusted. This helps platforms spotlight their most valuable reviewers.

<img width="695" height="470" alt="image" src="https://github.com/user-attachments/assets/356d68b7-bc39-491f-b1f4-694aceebd583" />

## 🎯 Why This Matters

A Reviewer Trust Score helps platforms:
  - Highlight trusted reviewers with badges or leaderboards.
  - Reduce spam and fake reviews by filtering low-trust accounts.
  - Build user confidence, making the platform more reliable.
## 🛠️ Tech Stack

  - **Python** : (pandas, numpy, scikit-learn, matplotlib)
  - **Dataset**: [Multilingual Mobile App Reviews (public Kaggle dataset)](https://www.kaggle.com/datasets/pratyushpuri/multilingual-mobile-app-reviews-dataset-2025?utm_source=chatgpt.com)
  - **Google Colab**: for development and reproducibility
  
## 🚀 Next Steps

  - Experiment with different weighting schemes.
  - Add NLP analysis of review text (e.g., sentiment, subjectivity).
  - Build an interactive dashboard to explore reviewer trust scores.

👉 This project shows how data science can be applied to real product problems — balancing technical modeling with product-driven KPIs.


  

