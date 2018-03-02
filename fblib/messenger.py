import requests

from fblib.core import FacebookError


def url_button():
    return {
        'type':"web_url",
        'url":"<URL_TO_OPEN>",
        'title":"<BUTTON_TEXT>",
        'webview_height_ratio": "<compact|tall|full>",
        'messenger_extensions": "<true|false>",  
        'fallback_url": "<URL_TO_FALLBACK_TO>"
    }


class BotAPI:
    api_url = 'https://graph.facebook.com'
    api_version = 'v2.6'

    def __init__(self, access_token):
        self.access_token = access_token

    def _call_api(self, http_method, api_method, json=None, files=None, **kwargs):
        """ Basic method for calling Facebook Messenger Api
            Required parameters:
                http_method -- HTTP request methods, e.g. 'POST', 'GET', etc.
                api_method -- part of URL after `self.api_url`
            Optional parameters:
                kwargs -- dictionary that specifying additional data to send
                          to the server
        """
        url = '/'.join((self.api_url, self.api_version, api_method))
        params = dict(access_token=self.access_token)
        params.update(kwargs)
        res = requests.request(http_method, url, params=params, files=files, json=json)
        if hasattr(res.json, '__contains__') and 'error' in res.json:
            raise FacebookError(res.json)
        return res

    def send_message(self, recipient_id, message):
        api_method = 'me/messages'
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message
            }
        }
        return self._call_api('POST', api_method, json=payload)
