import logging
from newsconnector.support.similar import (
    build_similar, get_ratio, get_fuzzy_ratio)
from newsconnector.support.test_data import news_data, headlines_data
logging.disable(logging.CRITICAL)
from unittest import TestCase


class SimilarTest(TestCase):
    def test_number_of_items(self):
        result = build_similar(news_data['articles'], 'newsarticle')
        self.assertEqual(len(news_data['articles']), 40)
        self.assertEqual(len(result), 30)

    def test_similar_ratio(self):
        arts = headlines_data['articles']

        r = get_ratio(arts[0], arts[0]['similar'][0])
        f = get_fuzzy_ratio(arts[0], arts[0]['similar'][0])
        self.assertTrue(f > r)

    def test_using_fuzz(self):
        arts = headlines_data['articles']
        f_similar = []
        l_similar = []
        for art in arts[0]['similar']:
            #score = fuzz.token_set_ratio(arts[0]['fulltext'], art['fulltext'])
            fuzzy_score = get_fuzzy_ratio(arts[0], art)
            lev_score = get_ratio(arts[0], art)
            if fuzzy_score >= 70:
                f_similar.append(art['title'])
            if lev_score >= 0.40:
                l_similar.append(art['title'])

        self.assertFalse(set(f_similar) - set(l_similar))
        self.assertEqual(len(f_similar), 7)
        self.assertEqual(len(l_similar), 43)

    def test_null_articles(self):
        arts = headlines_data['articles']
        self.assertEqual(get_ratio(arts[0], None), 0)
        self.assertEqual(get_ratio(None, arts[0]), 0)

        self.assertEqual(get_fuzzy_ratio(None, arts[0]), 0)
        self.assertEqual(get_fuzzy_ratio(arts[0], None), 0)
