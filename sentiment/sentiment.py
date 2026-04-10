from textblob import TextBlob

def analyze_sentiment(reviews):

    combined = " ".join(reviews)

    analysis = TextBlob(combined)

    score = analysis.sentiment.polarity

    return score