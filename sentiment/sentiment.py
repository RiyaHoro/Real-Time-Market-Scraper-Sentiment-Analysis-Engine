from textblob import TextBlob


def analyze_sentiment(reviews):

    scores = []

    for review in reviews:
        polarity = TextBlob(review).sentiment.polarity
        scores.append(polarity)

    sentiment = sum(scores) / len(scores)

    return sentiment