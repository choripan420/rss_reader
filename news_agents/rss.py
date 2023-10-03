import feedparser
import trafilatura
import pickle

class FeedReader:
    def __init__(self, url):
        self.url = url
        try:
            feed = feedparser.parse(self.url)
            # A simple check to see if we got valid feed data
            if not feed.entries:
                raise ValueError("Invalid feed data")
        except:
            print('Getting RSS failed. Using mocked response instead.')
            with open('bbc_feed.pkl', 'rb') as file:
                feed = pickle.load(file)

        self.feed = [
            {
                key: entry.get(key, None)
                for key in ["title", "summary", "link", "published"]
            }
            for entry in feed.entries
        ]

    def read_article(self, index):
        try:
            article_url = self.feed[index]["link"]
            downloaded = trafilatura.fetch_url(article_url)
            text = trafilatura.extract(downloaded)
            return {
                "metadata": self.feed[index],
                "body": text,
            }
        except Exception as e:
            return {
                "error": str(e),
            }
        

reader = FeedReader("http://feeds.bbci.co.uk/news/rss.xml")
