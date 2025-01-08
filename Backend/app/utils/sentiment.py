from textblob import TextBlob

def detect_sentiment(text: str):
    analysis = TextBlob(text)
    return {"polarity": analysis.sentiment.polarity, "subjectivity": analysis.sentiment.subjectivity}
