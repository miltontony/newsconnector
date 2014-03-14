import logging
from newsconnector.support.similar import build_similar, get_ratio, get_fuzzy_ratio
from newsconnector.support.test_data import news_data, headlines_data
from unittest import TestCase
logging.disable(logging.CRITICAL)


class SimilarTest(TestCase):
    def test_number_of_items(self):
        result = build_similar(news_data['articles'])

        self.assertEqual(len(news_data['articles']), 40)
        self.assertEqual(len(result), 27)

    def test_similar_ratio(self):
        arts = headlines_data['articles']

        print get_ratio(arts[0], arts[0]['similar'][0])
        print get_fuzzy_ratio(arts[0], arts[0]['similar'][0])

    def test_using_fuzz(self):
        arts = headlines_data['articles']
        print '--fuzz test--'
        print 'Title: ', arts[0]['title']
        for art in arts[0]['similar']:
            #score = fuzz.token_set_ratio(arts[0]['fulltext'], art['fulltext'])
            score = get_fuzzy_ratio(arts[0], art)
            if score < 70:
                n = '***' + art['title']
            else:
                n = art['title']
            print art['score'], ' vs ', score, ' - ', n

        print '--end--'
        #print get_ratio(arts[0]['fulltext'], arts[2]['fulltext'])
        #self.assertFalse(result[0]['similar'][0]['score'] >= 0.55)
