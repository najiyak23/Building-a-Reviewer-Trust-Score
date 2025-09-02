import pandas as pd
import kagglehub

# Download latest version
path = kagglehub.dataset_download("pratyushpuri/multilingual-mobile-app-reviews-dataset-2025")

print("Path to dataset files:", path)
import os
print(os.listdir(path))

# Load the dataset into a DataFrame
df = pd.read_csv(path + "/multilingual_mobile_app_reviews_2025.csv")

# Inspect the shape and first few rows
print(df.shape)
df.head()

# Select only the columns we need
df = df[['user_id', 'review_text', 'rating', 'review_date', 
         'num_helpful_votes', 'verified_purchase']].copy()

# Rename for clarity
df.columns = ['reviewer_id', 'review_text', 'rating', 'review_date', 
              'helpful_votes', 'verified_purchase']

# Convert datatypes
df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Drop missing values in critical columns
df = df.dropna(subset=['reviewer_id', 'review_text', 'rating', 'review_date'])

# Clip ratings between 1 and 5
df['rating'] = df['rating'].clip(1, 5)

# Add review length feature
df['review_length_words'] = df['review_text'].astype(str).str.split().map(len)

df.head()

import numpy as np

# Group by reviewer
reviewer_stats = df.groupby('reviewer_id').agg(
    num_reviews = ('review_text', 'count'),
    avg_rating = ('rating', 'mean'),
    rating_stddev = ('rating', 'std'),
    avg_review_length = ('review_length_words', 'mean'),
    avg_helpful_votes = ('helpful_votes', 'mean'),
    verified_ratio = ('verified_purchase', 'mean'),
    last_review_date = ('review_date', 'max')
).reset_index()

# Handle NaNs (e.g. stddev for single review users)
reviewer_stats['rating_stddev'] = reviewer_stats['rating_stddev'].fillna(0)

# Add recency feature (reviews in last 180 days)
cutoff_date = df['review_date'].max() - pd.Timedelta(days=180)
recent_reviews = df[df['review_date'] >= cutoff_date].groupby('reviewer_id').size()
reviewer_stats['recent_reviews'] = reviewer_stats['reviewer_id'].map(recent_reviews).fillna(0)

reviewer_stats.head()
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

# Pick features we want in the Trust Score
features = ['num_reviews','avg_rating','rating_stddev',
            'avg_review_length','avg_helpful_votes',
            'verified_ratio','recent_reviews']

reviewer_stats_scaled = reviewer_stats.copy()
reviewer_stats_scaled[features] = scaler.fit_transform(reviewer_stats[features])

reviewer_stats_scaled.head()
# Define weights
weights = {
    'num_reviews': 0.2,
    'rating_stddev': 0.15,
    'avg_review_length': 0.1,
    'avg_helpful_votes': 0.25,
    'verified_ratio': 0.15,
    'recent_reviews': 0.15
}

# Compute trust score
reviewer_stats_scaled['trust_score'] = (
    reviewer_stats_scaled['num_reviews'] * weights['num_reviews'] +
    reviewer_stats_scaled['rating_stddev'] * weights['rating_stddev'] +
    reviewer_stats_scaled['avg_review_length'] * weights['avg_review_length'] +
    reviewer_stats_scaled['avg_helpful_votes'] * weights['avg_helpful_votes'] +
    reviewer_stats_scaled['verified_ratio'] * weights['verified_ratio'] +
    reviewer_stats_scaled['recent_reviews'] * weights['recent_reviews']
)

# Sort reviewers by trust
leaderboard = reviewer_stats_scaled.sort_values('trust_score', ascending=False)
leaderboard.head(10)
import matplotlib.pyplot as plt

# Pick top 10 reviewers
top10 = leaderboard.head(10)

plt.figure(figsize=(10,6))
plt.barh(top10['reviewer_id'].astype(str), top10['trust_score'], color='skyblue')
plt.xlabel("Trust Score")
plt.ylabel("Reviewer ID")
plt.title("Top 10 Most Trusted Reviewers")
plt.gca().invert_yaxis()  # highest at top
plt.show()

plt.figure(figsize=(8,5))
plt.hist(leaderboard['trust_score'], bins=30, color='purple', alpha=0.7)
plt.xlabel("Trust Score")
plt.ylabel("Number of Reviewers")
plt.title("Distribution of Reviewer Trust Scores")
plt.show()

