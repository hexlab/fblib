"""
fblib - Facebook Python SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Alternative version of Facebook Python SDK for Facebook Graph API.
Based on Requests library (https://github.com/kennethreitz/requests).

Basic UserAPI usage:

    >>> from fblib import core
    >>> access_token = 'AAACEdEose0cBANLuYDa229TKr74oI6UYZC3BTZA...'
    >>> api = core.UserAPI(access_token)
    >>> api.get_objects('me')
    {...dictionary with users data from Facebook Graph API...}

Basic AppAPI usage:
    >>> from fblib import core
    >>> app_id='390492104572701'
    >>> app_secret='5afa25cc01ea0440c340e20e2c6a8df'
    >>> api = core.AppAPI(app_id=app_id, app_secret=app_secret)
    >>> app_api.get_app_access_token()
    7667gh5465g67jhj888

Running tests:
    python tests.py --access_token=AAACEdEose0cBANLuYDa229TKr74oI6UYZC3BTZA...
        --app_id=390492104572701 --app_secret=5afa25cc01ea0440c340e20e2c6a8df

:copyright: (c) 2012 by Kirill Karmadonov.
:license: ISC, see LICENSE for more details.
"""

__title__ = 'fblib'
__version__ = (0, 9, 5)
__author__ = 'Kirill Karmadonov'
__license__ = 'ISC'
__copyright__ = 'Copyright 2012 Kirill Karmadonov'
