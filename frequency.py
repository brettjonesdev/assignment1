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


def get_terms_from_tweets(tweets):
    all_terms_count = 0
    all_terms = {}
    for tweet in tweets:
        terms = re.findall(r"\w+", tweet)
        for term in terms:
            all_terms_count += 1
            if term in all_terms:
                all_terms[term] += 1
            else:
                all_terms[term] = 1

    return all_terms, all_terms_count


def main():
    tweet_file = open(sys.argv[1])

    tweets = get_tweets_from_file(tweet_file)
    all_terms, all_terms_count = get_terms_from_tweets(tweets)
    for term, count in all_terms.iteritems():
        print '%s %f' % (term, float(count) / all_terms_count)

if __name__ == '__main__':
    main()
