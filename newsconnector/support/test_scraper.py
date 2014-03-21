import logging
logging.disable(logging.CRITICAL)
from newsconnector.support.utils import scrape
from unittest import TestCase


class ScraperTest(TestCase):
    def test_news24(self):
        text = scrape('http://www.news24.com/SouthAfrica/News/R25m-worth-of-counterfeit-CDs-seized-20140320')
        print text
        self.assertTrue('producing the fake CDs' in text)

    def test_sowetan(self):
        text = scrape('http://www.sowetanlive.co.za/news/2014/03/14/oscar-trial-first-cop-ignorant-about-window')
        print text
        self.assertTrue('Botha was replaced' in text)

    def test_timeslive(self):
        text = scrape('http://www.timeslive.co.za/world/2014/03/20/more-eu-sanctions-on-russia-g-8-suspended-merkel')
        print text
        self.assertTrue('United States slapped sanctions' in text)

    def test_ewn(self):
        text = scrape('http://ewn.co.za/2014/03/21/Police-hunt-for-Bosmont-school-robbers')
        print text
        self.assertTrue('The pair targeted school officials' in text)

    def test_newage(self):
        text = scrape('http://www.thenewage.co.za/Detail.aspx?news_id=121438&cat_id=1007')
        print text
        self.assertTrue('KwaZulu-Natal transport' in text)

    def test_moneyweb(self):
        text = scrape('http://www.moneyweb.co.za/moneyweb-financial/rand-slips-against-dollar-2')
        print text
        self.assertTrue('consumer inflation data for February' in text)

    def test_sport24(self):
        text = scrape('http://www.sport24.co.za/Golf/PGATour/Scott-sizzles-at-Bay-Hill-20140321')
        print text
        self.assertTrue('World No 2 Scott' in text)

    def test_supersport(self):
        text = scrape('http://www.supersport.com/motorsport/article.aspx?Id=2367604')
        print text
        self.assertTrue('Agag told AFP that people' in text)

    def test_eonline(self):
        text = scrape('http://www.eonline.com/news/523549/shirtless-andrew-garfield-hits-the-waves-to-teach-autistic-kids-how-to-surf-swoon-alert?cmpid=rss-000000-rssfeed-365-topstories&utm_source=eonline&utm_medium=rssfeeds&utm_campaign=rss_topstories')
        print text
        self.assertTrue('Because his girlfriend' in text)
