#!/usr/bin/env python
import argparse
import unittest

from core import AppAPI, UserAPI, FacebookError

app_id = None
app_secret = None
access_token = None


class TestFacebookError(unittest.TestCase):

    def test_error_messages(self):
        access_token = 'Wrong'
        api = UserAPI(access_token)
        with self.assertRaises(FacebookError) as fe:
            api.get_objects('me')
        error = fe.exception.value['error']
        self.assertIn('message', error)
        self.assertIn('code', error)
        self.assertIn('type', error)
        self.assertEqual(error['code'], 190)
        self.assertEqual(error['type'], 'OAuthException')


class TestAppAPI(unittest.TestCase):

    def setUp(self):
        self.api = AppAPI(app_id, app_secret)

    def test_default_workflow(self):

        # get app access token
        res = self.api.get_app_access_token()
        self.assertTrue(res)

        # get list of test users assigned to the application
        res = self.api.get_list_of_test_users()
        print('======>>>', res)
        self.assertIn('data', res)
        test_users = len(res['data'])

        # create test user
        res = self.api.create_test_user(name='Serg Ivanov')
        self.assertIn('access_token', res)
        self.assertIn('password', res)
        self.assertIn('login_url', res)
        self.assertIn('id', res)
        self.assertIn('email', res)

        res2 = self.api.get_list_of_test_users()
        self.assertEqual(test_users + 1, len(res2['data']))

        # delete test user
        user_api = UserAPI(res['access_token'])
        user_api.delete('me')

        res = self.api.get_list_of_test_users()
        self.assertEqual(test_users, len(res['data']))


class TestUserAPI(unittest.TestCase):

    def setUp(self):
        self.api = UserAPI(access_token)

    def test_default_workflow(self):

        # get information about user
        res = self.api.get_objects('me')
        self.assertIn('name', res)
        self.assertIn('id', res)

        # get information about user education and first_name
        res = self.api.get_objects('me', fields='first_name')
        self.assertIn('first_name', res)

        # get 10 friends
        res = self.api.get_connections('me', 'friends', limit=10)
        self.assertIn('data', res)
        self.assertEqual(res['data'], [])

        # Get next 10 friends
        if 'paging' in res and 'next' in res['paging']:
            res = self.api.get_connections('me', 'friends', limit=10,
                offset=10)
            self.assertIn('paging', res)
            self.assertIn('data', res)
            self.assertEqual(len(res['data']), 10)

    def test_publish(self):
        # Publish post
        res = self.api.publish('me', 'feed', message='I like this new API!')
        self.assertIn('id', res)
        post_id = res['id']
        # Delete post
        res = self.api.delete(post_id)


parser = argparse.ArgumentParser(description='Test fblib')
parser.add_argument('--app_id',
                    help='Facebook App ID',
                    required=True)
parser.add_argument('--app_secret',
                    help='Facebook App secret',
                    required=True)
parser.add_argument('--access_token',
                    help='Facebook user access token. '
                         'You could generate one here: '
                         'https://developers.facebook.com/tools/access_token/',
                    required=True)


if __name__ == '__main__':
    args = parser.parse_args()

    app_id = args.app_id
    app_secret = args.app_secret
    access_token = args.access_token

    suite = unittest.TestSuite()
    test_methods = (TestFacebookError('test_error_messages'),
                    TestAppAPI('test_default_workflow'),
                    TestUserAPI('test_default_workflow'))
    suite.addTests(test_methods)
    unittest.TextTestRunner().run(suite)
