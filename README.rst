fblib: Facebook Python SDK
==========================

Alternative unofficial version of Facebook Python SDK for Facebook Graph API. Based on `Requests <https://github.com/kennethreitz/requests>`_ library. You can read more about the Graph API by accessing its `official documentation <https://developers.facebook.com/docs/reference/api/>`_.

Usage
-----

Basic UserAPI usage::

    import fblib
    api = fblib.core.UserAPI(<user_access_token>)
    api_user = api.get_objects('me')

Basic AppAPI usage::

    import fblib
    api = fblib.core.AppAPI(app_id=<application_id>, app_secret=<application_key>)
    app_token = app_api.get_app_access_token()

Proper usage::

    import fblib
    access_token = <user_access_token>
    api = fblib.core.UserAPI(access_token)
    try:
        api_user = api.get_objects('me')
    except fblib.core.FacebookError:
        <handling exception>

Functional testing
------------------

Running tests::

    python tests.py --access_token=AAACEdEose0cBANLuYDa229TKr74oI6UYZC3BTZA --app_id=390492104572701 --app_secret=5afa25cc01ea0440c340e20e2c6a8df

Contributing
------------

- check for open issues or open a fresh issue
- when commiting, use `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_ and `0xCodeStyle <https://github.com/0xKirill/0xCodeStyle>`_
- write a test which shows that the bug was fixed or that the feature works as expected
- add yourself to AUTHORS
- send a pull request and wait until it will be merged

Report Issues/Bugs
------------------

For library bugs: https://github.com/0xKirill/fblib/issues

For Facebook Graph API bugs: https://developers.facebook.com/bugs

Facebook Graph API QA: http://facebook.stackoverflow.com/
