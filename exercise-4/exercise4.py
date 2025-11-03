import sqlite3
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
import nltk
import re

import matplotlib.pyplot as plt

DATABASE = "database.sqlite"
con = sqlite3.connect(DATABASE)
cur = con.cursor()

def exercise1():
    print("EXERCISE 1 BEGINNING")

    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')

    query = "SELECT content FROM posts UNION ALL SELECT content FROM comments"
    result = cur.execute(query)
    stop_words = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()

    bow_list = []

    for row in result:
        text = row[0]
        tokens = word_tokenize(text.lower())
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
        tokens = [t for t in tokens if len(t) > 2]
        tokens = [t for t in tokens if t.isalpha() and t not in stop_words]

        if len(tokens) > 0:
            bow_list.append(tokens)

    dictionary = Dictionary(bow_list)
    dictionary.filter_extremes(no_below=2, no_above=0.5)
    corpus = [dictionary.doc2bow(tokens) for tokens in bow_list]
    optimal_lda = None

    lda = LdaModel(corpus, num_topics = 10, id2word = dictionary, passes = 10, random_state = 2)
    coherence_model = CoherenceModel(model = lda, texts = bow_list, dictionary = dictionary, coherence = "c_v")
    coherence_score = coherence_model.get_coherence()

    print(f'Trained LDA with {10} topics. Average topic coherence: {coherence_score}')
    optimal_lda = lda

    topic_list = []
    for i, topic in optimal_lda.print_topics(num_words=5):
        print(f"Topic {i}: {topic}")
        topic_list.append(topic)
    return topic_list

def exercise2(topics):
    print("EXERCISE 2 BEGINNING")

    nltk.download('vader_lexicon')
    result = cur.execute("SELECT content FROM posts UNION ALL SELECT content FROM comments")
    rows = result.fetchall()
    df = pd.DataFrame(rows, columns=['content'])

    sia = SentimentIntensityAnalyzer()
    df['sentiment'] = df['content'].apply(lambda text: sia.polarity_scores(text)['compound'])
    mean_sentiment = df['sentiment'].mean()
    print(f"Platform mean sentiment: {mean_sentiment}")

    topics_regex = [' '.join(re.findall(r'"(.*?)"', t)) for t in topics]

    topic_sentiment_scores = [sia.polarity_scores(topic)['compound'] for topic in topics_regex]
    for i, score in enumerate(topic_sentiment_scores):
        print(f"Topic {i} sentiment score: {score}")

    topics_rewrite = [
        "Remember to keep your coffee habit this year for health",
        "The new music ended last night and I really like it",
        "I like how I tried a new sound for the next project",
        "The book let me see the world through another one’s eyes",
        "Let the real need for change make us think again",
        "It’s important to think and see what might shift your perspective",
        "I sometimes like people who get me serious, maybe",
        "This post really made me feel a hit of emotion",
        "I never get to see things totally like before, maybe",
        "I love to keep a great and curious spirit alive"
    ]

    print(" ") 

    topic_sentiment_scores_rewrite = [sia.polarity_scores(topic)['compound'] for topic in topics_rewrite]
    for i, score in enumerate(topic_sentiment_scores_rewrite):
        print(F"Topic {i} rewritten sentiment score: {score}")

if __name__ == "__main__":
    topics = exercise1()
    exercise2(topics)
