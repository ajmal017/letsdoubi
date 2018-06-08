class TweetSentiment(object):
    def __init__(self, median, mean, count, plain_count):
        self.median = str(median)
        self.mean = str(mean)
        self.count = str(count)
        self.plain_count = str(plain_count)
