import sys
import re
import json

def get_dictionary(file):
    dictionary = {}
    for line in file:
        term, score = line.split("\t")
        dictionary[term] = int(score)

    return dictionary


def get_sentiment_score(tweet, dictionary):
    score = 0
    terms = re.findall(r"\w+", tweet)
    for term in terms:
        if term in dictionary:
            score += dictionary[term]

    return score


def get_tweet_text_from_file(file):
    texts = []
    for line in file:
        obj = json.loads(line)
        if 'text' in obj:
            texts.append(obj['text'])

    return texts


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiment_dictionary = get_dictionary(sent_file)

    tweets = get_tweet_text_from_file(tweet_file)

    for tweet in tweets:
        print get_sentiment_score(tweet, sentiment_dictionary)

if __name__ == '__main__':
    main()
