from newsconnector.support.similar import build_similar
from django.test import TestCase


arts = [{
    'image_url': "",
    'hash_key': "9264c755745e76e419eeab0e398f4bd1",
    'date_iso': "2013-07-02T17:58:00",
    'title': "Judgement reserved in Breytenbach case",
    'content': "Judgment on prosecutor Glynnis Breytenbach's application to be reinstated to her job was reserved by the Labour Court in Johannesburg on Tuesday",
    'date': "5 days, 20 hours ago",
    'score': None,
    'link': "http://www.thenewage.co.za/Detail.aspx?news_id=100212&cat_id=1007",
    'source': "thenewage.co.za",
    'keywords': [
    "labour court in johannesburg",
    "government",
    "law_crime",
    "glynnis breytenbach",
    "law",
    "labour court",
    "prosecutor",
    "glynnis"
    ],
    'similar': [],
    'seen': [],
    },
    {
    'image_url': "http://www.timeslive.co.za/Feeds/2013/06/01/1028761_849410.jpg/ALTERNATES/crop_80x80/1028761_849410.jpg",
    'hash_key': "05a9c7293deecc1bdb680e1692db9f32",
    'date_iso': "2013-07-02T16:49:04",
    'title': "Breytenbach position not affected: lawyer",
    'content': "The transfer of prosecutor Glynnis Breytenbach does not take away the position she held before, the Labour Court in Johannesburg heard on Tuesday.",
    'date': "1 hour, 48 minutes ago",
    'score': None,
    'link': "http://www.timeslive.co.za/local/2013/07/02/breytenbach-position-not-affected-lawyer",
    'source': "timeslive.co.za",
    'keywords': [
    "labour court in johannesburg",
    "breytenbach",
    "lawyer",
    "glynnis breytenbach",
    "labour court",
    "prosecutor",
    "glynnis"
    ],
    'seen': [],
    'similar': [ ]
    },
    {
    'image_url': "",
    'hash_key': "5d167ebc30efe2ecb9a21583d1ba8c13",
    'date_iso': "2013-07-02T17:46:04",
    'title': "Public not fooled by e-toll tariffs: Outa",
    'content': "The public is not fooled by the reduced e-toll tariffs, the Opposition to Urban Tolling Alliance (Outa) said on Tuesday",
    'date': "5 days, 20 hours ago",
    'score': None,
    'link': "http://www.thenewage.co.za/Detail.aspx?news_id=100209&cat_id=1007",
    'source': "thenewage.co.za",
    'keywords': [
    "toll road",
    "environment",
    "international trade",
    "urban tolling alliance",
    "tariff",
    "e-toll"
    ],
    'seen': [],
    'similar': []
}]


class SimilarTest(TestCase):
    def test_number_of_items(self):
        result = build_similar(arts)

        self.assertEqual(len(arts), 3)
        self.assertEqual(len(result), 2)

    def test_similar_ratio(self):
        result = build_similar(arts)

        #1 item is similar
        self.assertEqual(len(result[0]['similar']), 1)

        #
        self.assertTrue(result[0]['similar'][0]['score'] >= 0.55)
