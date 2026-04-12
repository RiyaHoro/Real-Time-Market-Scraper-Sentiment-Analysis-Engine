import subprocess

def get_sentiment(reviews):

    review_string = "|".join(reviews)

    result = subprocess.run(
        ["Rscript", "r/sentiment.R", review_string],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()

    if output == "" or output == "NA":
        sentiment_score = 0.0
    else:
        sentiment_score = float(output)

    return sentiment_score