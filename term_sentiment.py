import sys
import json
import re


def get_tweets_from_file(tweet_file):
    tweets = []
    for line in tweet_file:
        obj = json.loads(line)
        if 'text' in obj:
            tweets.append(obj['text'])
    return tweets


def get_sentiment_dict(dictFile):
    dictionary = {}
    for line in dictFile:
        term, score = line.split("\t")
        dictionary[term] = int(score)

    return dictionary


def get_tweet_sentiment_obj(terms, dict, prior_obj):
    pos_terms = 0
    neg_terms = 0

    for term in terms:
        if term in dict:
            if dict[term] > 0:
                pos_terms += 1
            elif dict[term] < 0:
                neg_terms += 1

    pos = (pos_terms > 0)
    neg = (neg_terms > 0)

    if prior_obj:
        result = prior_obj
    else:
        result = {'pos': 0, 'neg': 0, 'uses': 0}

    if pos:
        result['pos'] += 1
    elif neg:
        result['neg'] += 1

    result['uses'] += 1

    return result


def find_non_sentiment_carrying_words(tweets, sentiments):
    non_sentiment_carrying_dict = {}

    for tweet in tweets:
        terms = re.findall(r"\w+", tweet)
        for term in terms:
            if term not in sentiments and len(term) > 1:
                if term in non_sentiment_carrying_dict:
                    previous_sentiment_obj = non_sentiment_carrying_dict[term]
                    sentiment_obj = get_tweet_sentiment_obj(terms, sentiments, previous_sentiment_obj)
                else:
                    sentiment_obj = get_tweet_sentiment_obj(terms, sentiments, False)

                non_sentiment_carrying_dict[term] = sentiment_obj

    return non_sentiment_carrying_dict


def main():
    sentiment_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    tweets = get_tweets_from_file(tweet_file)
    sentiments = get_sentiment_dict(sentiment_file)
    non_sentiment_carrying_words_dict = find_non_sentiment_carrying_words(tweets, sentiments)

    for term, count_obj in non_sentiment_carrying_words_dict.iteritems():
        pos = count_obj['pos']
        neg = count_obj['neg']
        uses = count_obj['uses']

        ratio = 100 * (1 + float(pos)/uses - float(neg)/uses)

        print '%s\t%0.2f' % (term, ratio)

if __name__ == '__main__':
    main()
