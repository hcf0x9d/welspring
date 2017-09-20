import feedparser
import datetime

from model import Base, Data
from db_controller import session, DatabaseController

devotion_feed = "https://wels.net/dev-daily/feed/pt-dev-daily/?redirect=no"
# devotion_feed = "http://feeds.feedburner.com/hl-devos-votd"
now = datetime.datetime.now()
date_now = now.strftime("%Y-%m-%d")
dbc = DatabaseController()


class FeedReader:

    def start(self):
        if self.check_date() is not True:
            feed = self.fetch_feed()
            self.store_feed(feed)
            print('api hit')
            return feed
        else:
            return self.fetch_feed_db()

    def check_date(self):
        try:
            session.query(Data).filter_by(type='devotion', date=date_now).one()
            return True
        except:
            return False

    def fetch_feed_db(self):
        return session.query(Data).filter_by(type='devotion',
                                             date=date_now).one()

    def fetch_feed(self):
        return feedparser.parse(devotion_feed)

    def store_feed(self, obj):
        # TODO: Store the feed into
        title = obj.entries[0]['title']
        subtitle = obj.entries[0]['subtitle']
        body = obj.entries[0].content[0]['value']
        dbc.create_data_entry('devotion', date_now, title, subtitle, body)
        return
