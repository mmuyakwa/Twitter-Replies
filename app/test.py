import unittest
import tweepy
from decouple import config

class TestTweepy(unittest.TestCase):

    def test_tweepy(self):
        auth = tweepy.OAuthHandler(config('CONSUMER_KEY'), config('CONSUMER_SECRET'))
        auth.set_access_token(config('OAUTH_TOKEN'), config('OAUTH_TOKEN_SECRET'))
        api = tweepy.API(auth, wait_on_rate_limit=True)
        user = api.get_user('ibm_root')
        print(user.id)
        self.assertTrue((user.id == 14912427))

if __name__ == '__main__':
    unittest.main()