# -*- coding: utf-8 -*-
"""Book Recommendation System"""

import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction import text

# Load dataset
bookrecdata = pd.read_csv('GoodReads_100k_books.csv')

# Preprocess genre
bookrecdata['clean_genre'] = bookrecdata['genre'].fillna("")
comma_tokenizer = lambda t: [g.strip() for g in t.split(',')]
tfidf_vec_genre = TfidfVectorizer(tokenizer=comma_tokenizer, lowercase=True)
tfidf_matrix_genre = tfidf_vec_genre.fit_transform(bookrecdata['clean_genre'])

# Preprocess description/text
bookrecdata['desc'] = bookrecdata['desc'].fillna('')
bookrecdata['title'] = bookrecdata['title'].fillna('')

# Merge title + description (for better recommendations)
bookrecdata['text'] = bookrecdata['title'] + ' ' + bookrecdata['desc']

# Stopwords
default_stopwords = text.ENGLISH_STOP_WORDS
custom_stopwords = {'book', 'honor', 'notable', 'award', 'caldecott', 'ala'}
all_stopwords = default_stopwords.union(custom_stopwords)

tfidf_vec_text = TfidfVectorizer(
    stop_words=list(all_stopwords),
    max_features=5000,
    sublinear_tf=True
)
tfidf_text = tfidf_vec_text.fit_transform(bookrecdata['text'])

# Author encoding
bookrecdata['author'] = bookrecdata['author'].fillna('Unknown')
count_vec_author = CountVectorizer(token_pattern=r'.+', lowercase=False)
author_features = count_vec_author.fit_transform(bookrecdata['author'])

# Ratings + Reviews
ratings = bookrecdata['rating'].fillna(0).values.reshape(-1, 1)
reviews = bookrecdata['reviews'].fillna(0).values.reshape(-1, 1)

scaler = MinMaxScaler()
rating_features = scaler.fit_transform(ratings)
review_features = scaler.fit_transform(reviews)

# Weightage
w_genre = 2
w_desc = 2
w_author = 0.5
w_ratings = 3
w_reviews = 0.5

combined_features = hstack([
    tfidf_matrix_genre * w_genre,
    tfidf_text * w_desc,
    author_features * w_author,
    rating_features * w_ratings,
    review_features * w_reviews
]).tocsr()

# Recommendation function
def recommend_books(book_title, top_n=10):
    matches = bookrecdata[bookrecdata['title'].str.contains(book_title, case=False, na=False)]
    if matches.empty:
        return f"No book found with title matching '{book_title}'"

    target_index = matches.index[0]
    sim_scores = linear_kernel(combined_features[target_index], combined_features).flatten()
    top_indices = sim_scores.argsort()[::-1][1:top_n+1]
    similar_books = bookrecdata.iloc[top_indices][['title', 'author', 'rating']]

    return similar_books.reset_index(drop=True)



if __name__ == "__main__":
    print("\nRecommendations:\n")
    targetbook=input("Enter the book you want to find: ")
    recs = recommend_books(targetbook)
    print(recs)
