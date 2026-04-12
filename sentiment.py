from textblob import TextBlob


def analyze_sentiment(text_list):

    scores = []

    for text in text_list:

        blob = TextBlob(text)

        scores.append(blob.sentiment.polarity)
    if scores:
        return sum(scores) / len(scores)
    else: 
        return 0 