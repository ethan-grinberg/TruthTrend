import tweepy


class TwitterBot:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet_article(self, title, url, keyword):
        keyword = keyword.replace(" ", "")
        tweet = title + ' #' + keyword + ' ' + url
        self.api.update_status(tweet)

    def tweet_all_articles(self, summarized_news):
        for i in range(0, len(summarized_news)):
            title = summarized_news.iloc[i].title
            url = summarized_news.iloc[i].url
            topic = summarized_news.iloc[i].topic

            self.tweet_article(title, url, topic)
