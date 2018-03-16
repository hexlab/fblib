import requests

from fblib.core import FacebookError


class SendAPI:
    api_url = 'https://graph.facebook.com'
    api_version = 'v2.6'

    def __init__(self, access_token):
        self.access_token = access_token

    def _call_api(self, http_method, api_method, json=None, files=None,
                  **kwargs):
        """ Basic method for calling Facebook Messenger Api

            Args:
                http_method:
                    HTTP request methods, e.g. 'POST', 'GET', etc.
                api_method:
                    part of URL after `self.api_url`
                kwargs:
                    dictionary that specifying additional data to send
                    to the server
        """
        url = '/'.join((self.api_url, self.api_version, api_method))
        params = dict(access_token=self.access_token)
        params.update(kwargs)
        res = requests.request(http_method, url, params=params, files=files,
                               json=json)
        if hasattr(res.json, '__contains__') and 'error' in res.json:
            raise FacebookError(res.json)
        return res

    def page_message_tags(self):
        """ Retrieve the current list of supported tags.
        """
        api_method = 'page_message_tags'
        return self._call_api('GET', api_method)

    def send_message(self, message):
        """

            Reference:
            https://developers.facebook.com/docs/messenger-platform/send-messages
        """
        api_method = 'me/messages'
        template = message.build() if hasattr(message, 'build') else message
        return self._call_api('POST', api_method, json=template)
