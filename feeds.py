import feedparser
import datetime

from twitter import *
from config import Config
from model import Data
from db_controller import session, DatabaseController

devotion_feed = "https://wels.net/dev-daily/feed/pt-dev-daily/?redirect=no"
verse_feed = "http://www.biblegateway.com/usage/votd/rss/votd.rdf?31"
now = datetime.datetime.now()
date_now = now.strftime("%Y-%m-%d")
dbc = DatabaseController()
config = Config()

twitter_api = Twitter(auth=OAuth(config.API_KEYS['twitter']['A_TOKEN'],
                                 config.API_KEYS['twitter']['A_SECRET'],
                                 config.API_KEYS['twitter']['C_KEY'],
                                 config.API_KEYS['twitter']['C_SECRET']))


class FeedReader:
    """This class is used to read feeds from online sources"""
    def __init__(self, feed_type):
        self.feed_type = feed_type

    def start(self):
        """Kick off the process of reading feeds

        :return: Feed object from the database or online
        """
        if self.check_date() is not True:
            feed = {}
            obj = self.fetch_feed()

            if self.feed_type == 'devotion':
                feed['title'] = obj.entries[0]['title']
                feed['subtitle'] = obj.entries[0]['subtitle']
                feed['body'] = obj.entries[0].content[0]['value']
            else:
                feed['title'] = 'Verse of the day'
                feed['subtitle'] = obj.entries[0]['title']
                feed['body'] = obj.entries[0]['content'][0]['value']

            self.store_feed(feed)
            return feed
        else:
            return self.fetch_feed_db();

    def check_date(self):
        """Using the date_now variable, see if we have this feed stored

        Check our DB records for this feed (matching type and date

        :return: Boolean (we have today's feed in the DB or not)
        """
        try:
            session.query(Data).filter_by(type=self.feed_type,
                                          date=date_now).one()
            return True
        except:
            return False

    def fetch_feed_db(self):
        """Get the feed from the database

        We have the feed in stock, look it up by date and feed type

        :return: Database object
        """
        return session.query(Data).filter_by(type=self.feed_type,
                                             date=date_now).one()

    def fetch_feed(self):
        """Grab the feed from the ATOM URL

        Grabs the raw XML data from the ATOM feed and returns a parsed object

        :return: parsed feed
        """
        if self.feed_type == 'devotion':
            return feedparser.parse(devotion_feed)
        else:
            return feedparser.parse(verse_feed)

    def store_feed(self, obj):
        """This isn't the best solution, but it works for now

        For now, we simply select which type of feed this is, and then
        separate out the different bits based on that. This is not "elegant"
        nor "great," but it's functional

        :param obj: feed object to parse and store
        :return:
        """
        # Use the DataBaseController to insert the item into a temporary row
        dbc.create_data_entry(self.feed_type, date_now, obj['title'],
                              obj['subtitle'], obj['body'])
        return


class Twitter:

    def get_tweets(self, account, count):
        t = twitter_api.statuses.user_timeline(screen_name=account, count=count)
        return t
