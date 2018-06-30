#!/usr/bin/env python
"""
facebooklib.core
~~~~~~~~~~~~~~~~

This module contains methods for direct interaction with Facebook Graph API.
TODO: batch requests and cookies
"""
import requests


class FacebookError(Exception):

    def __init__(self, value):
        self.value = value
        self.message = value.get('error')

    def __str__(self):
        return repr(self.message)


class GraphAPI:
    """ Facebook Graph API """
    api_url = 'https://graph.facebook.com'
    api_verion = 'v3.0'

    def _call(self, http_method, path, **params):
        """ Basic method for calling Facebook Graph Api
            Required parameters:
                http_method -- HTTP request methods, e.g. 'POST', 'GET', etc.
                path -- part of URL after `self.api_url`
            Optional parameters:
                kwargs -- dictionary that specifying additional data to send
                          to the server
        """
        url = '{}/{}'.format(self.api_url, path)
        res = requests.request(http_method, url, params=params)
        json_data = res.json()
        if 'error' in json_data:
            raise FacebookError(json_data)
        return json_data


class AppAPI(GraphAPI):
    """ Apps methods for Facebook Graph API
    The object is initialized with the `app access key` and `app secret key`
    Example:
        app_api = AppAPI(app_id='19619262701', app_secret='5afa235c1ea2c6a7df')
        app_access_token = app_api.get_app_access_token()
        analytics = app_api.analytics()
    """

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None

    def _get_access_token(self):
        """ Returns the current application access token being used by the SDK
        """
        params = dict(client_id=self.app_id,
                      client_secret=self.app_secret,
                      grant_type='client_credentials')
        json_data = self._call('GET', 'oauth/access_token', **params)
        self.access_token = json_data.get('access_token')
        return self.access_token

    def call(self, http_method, api_method, **kwargs):
        """ Basic method for calling Facebook Graph Api
            Required parameters:
                http_method -- HTTP request methods, e.g. 'POST', 'GET', etc.
                api_method -- part of URL after `self.api_url`
            Optional parameters:
                kwargs -- dictionary that specifying additional data to send
                          to the server
        """
        if not self.access_token:
            self._get_access_token()
        path = '/'.join((self.app_id, api_method))
        params = dict(access_token=self.access_token)
        params.update(kwargs)
        return self._call(http_method, path, **params)

    def get_app_access_token(self):
        """ Returns the current access token being used by the SDK.
        """
        return self.access_token or self._get_access_token()

    def analytics(self, metric=None, **kwargs):
        """ Returns detailed analytics about the demographics of your users and
            how users are sharing from your application.
            Optional parameters:
                metric -- filter analytics information by this metric
                kwargs -- dictionary with additional parameters for the request
        """
        api_method = 'insights'
        if metric:
            api_method = '/'.join((api_method, metric))
        return self.call('GET', api_method, **kwargs)

    def get_list_of_test_users(self, **kwargs):
        """ Returns list of Facebook Test Users for this application
            Optional parameters:
                kwargs -- dictionary with additional parameters for the request
        """
        api_method = 'accounts/test-users'
        return self.call('GET', api_method, **kwargs)

    def create_test_user(self, installed=True, name='John Smith',
                         locale='en_US', permissions=None, method='post',
                         **kwargs):
        """ Create Facebook Test User
            Optional parameters:
                installed -- boolean parameter to specify whether your app
                    should be installed for the test user at the time
                    of creation. It is true by default.
                name -- name for the test user you create. The specified name
                    will also be used in the email address assigned to the
                    test user.
                locale -- locale for the test user you create, the default is
                    en_US. The list of supported locales:
                    https://www.facebook.com/translations/FacebookLocales.xml
                permissions -- comma-separated list of extended permissions.
                    Your app is granted these permissions for the new test user
                    if installed is true.
                method -- post
                kwargs -- dictionary with additional parameters for the request
        """
        api_method = 'accounts/test-users'
        params = dict(installed=installed,
                      name=name,
                      locale=locale,
                      method=method)
        if permissions:
            params['permissions'] = permissions
        kwargs.update(params)
        return self.call('GET', api_method, **kwargs)


class UserAPI(GraphAPI):
    """ Users methods for Facebook Graph API
    """

    def __init__(self, access_token):
        """
        """
        self.access_token = access_token

    def call(self, http_method, api_method, **kwargs):
        """ Basic method for calling Facebook Graph Api
            Required parameters:
                http_method -- HTTP request methods, e.g. 'POST', 'GET', etc.
                api_method -- part of URL after `self.api_url`
            Optional parameters:
                kwargs -- dictionary that specifying additional data to send
                          to the server
        """
        params = dict(access_token=self.access_token)
        params.update(kwargs)
        return self._call(http_method, api_method, **params)

    def get_objects(self, object_id, **kwargs):
        """ Returns object from Facebook Graph API

            Required parameters:
                object_id -- ID of object in the social graph, e.g: 'me',
                             '0xKirill', '0xKirill/picture', '817129783203'
            Optional parameters:
                kwargs -- dictionary with additional parameters for the request
        """
        api_method = '{}'.format(object_id)
        return self.call('GET', api_method, **kwargs)

    def get_connections(self, object_id, connection, **kwargs):
        """ Returns connections between objects

            Required parameters:
                object_id -- ID of object in the social graph, e.g., 'me',
                            '0xKirill', '0xKirill/picture', '817129783203'
                connection -- type of connection, e.g., 'friends', 'home',
                            'likes', 'movies', 'music', 'permissions', etc.
            Optional parameters:
                kwargs -- dictionary with additional parameters for the request
        """
        api_method = '{}/{}'.format(object_id, connection)
        return self.call('GET', api_method, **kwargs)

    def publish(self, object_id, connection, **kwargs):
        """ Publish to the Facebook graph
            Required parameters:
                object_id -- ID of object in the social graph, e.g., 'me',
                            '0xKirill', '0xKirill/picture', '817129783203'
                connection -- type of connection, e.g., 'feed', 'comments',
                            'likes', 'notes', 'links', 'events', etc.
            Optional parameters:
                kwargs -- dictionary with additional parameters for the request
        """
        api_method = '{}/{}'.format(object_id, connection)
        return self.call('POST', api_method, **kwargs)

    def delete(self, object_id):
        """ Delete objects in the graph
            Required parameters:
                object_id -- ID of object in the social graph, e.g., 'me',
                            '0xKirill', '0xKirill/picture', '817129783203'
        """
        api_method = '{}'.format(object_id)
        return self.call('DELETE', api_method)
