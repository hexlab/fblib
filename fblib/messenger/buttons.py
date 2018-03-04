from enum import Enum
from typing import Optional, List

from fblib.messenger.templates import *
from fblib.messenger.common import Button, RequestConstructor


class URLButton(Button):
    """ The URL Button opens a webpage in the Messenger webview.
        This button can be used with the Button and Generic Templates.

        Args:
            title:
                Button title. 20 character limit.
            url:
                This URL is opened in a mobile browser when the button is
                tapped.
                Must use HTTPS protocol if `messenger_extensions` is true.
            webview_height_ratio:
                Height of the Webview.
                Valid values: compact, tall, full. Defaults to full.
            messenger_extensions:
                Must be true if using Messenger Extensions.
            fallback_url:
                The URL to use on clients that don't support
                Messenger Extensions.
                If this is not defined, the url will be used as the fallback.
                It may only be specified if messenger_extensions is true.
            webview_share_button:
                Set to hide to disable the share button in the Webview
                (for sensitive info).
                This does not affect any shares initiated by the developer
                using Extensions

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/buttons/url
    """
    type_ = 'web_url'
    templates = [Button, GenericTemplate]

    def __init__(self,
                 title: str,
                 url: str,
                 webview_height_ratio: Optional[str]=None,
                 messenger_extensions: Optional[bool]=None,
                 fallback_url: Optional[str]=None,
                 webview_share_button: Optional[str]=None):
        self.syntax = {
            "type": self.type_,
            "url": url,
            "title": title,
            "webview_height_ratio": webview_height_ratio,
            "messenger_extensions": messenger_extensions,
            "fallback_url": fallback_url,
            "webview_share_button": webview_share_button,
        }


class PostbackButton(Button):
    """ When the postback button is tapped, the Messenger Platform
        sends an event to your postback webhook. This is useful when
        you want to invoke an action in your bot.
        This button can be used with the Button Template and Generic Template.

        Args:
            title:
                Button title. 20 character limit.
            payload:
                This data will be sent back to your webhook.
                1000 character limit.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/buttons/postback
    """
    type_ = 'postback'
    templates = [Button, GenericTemplate]

    def __init__(self, title: str, payload: str):
        self.syntax = {
            'type': self.type_,
            'title': title,
            'payload': payload
        }


class ShareButton(Button):
    """ The share button allows the message recipient to share the content
        of a message you sent with others on Messenger.
        The name and icon of your Page appear as an attribution at the top
        of the shared content. The attribution opens a conversation with
        your bot when tapped.

        With the share button, you can share the exact message or specify
        a new generic template message in the share_contents property.
        If you specify a new generic template, the message recipient will
        be able to add a message to the share. This is useful if you want
        change the look or add content to the original message.

        Args:
            share_contents:
                The message that you wish the recipient of the share to see,
                if it is different from the one this button is attached to.
                The format follows that used in Send API.

                share_contents only supports the following:
                    Template used must be generic template.
                    Maximum of one URL button on the template.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/buttons/share
    """
    type_ = 'element_share'
    templates = [GenericTemplate, ListTemplate, MediaTemplate]

    def __init__(self,
                 share_contents: Optional[GenericTemplate]=None):
        self.syntax = {
            'type': self.type_,
            'title': share_contents,
        }


class PaymentType(Enum):
    FIXED_AMOUNT = 'FIXED_AMOUNT'
    FLEXIBLE_AMOUNT = 'FLEXIBLE_AMOUNT'


class PriceList(RequestConstructor):
    """ List of objects used to calculate total price.
        Each label is rendered as a line item in the checkout dialog.

        Args:
            label:
                Label for line item.
            amount:
                Amount of line item.
    """

    def __init__(self, label: str, amount: str):
        self.syntax = {
            'label': label,
            'amount': amount
        }


class PaymentSummary(RequestConstructor):
    """ Fields used in the checkout dialog.

        Args:
            currency:
                Currency for price.
            payment_type:
                Must be FIXED_AMOUNT or FLEXIBLE_AMOUNT.
            merchant_name:
                Name of merchant.
            requested_user_info:
                Information requested from person
                that will render in the dialog.
                Valid values:
                    hipping_address, contact_name, contact_phone, contact_email
                You can config these based on your product need.
            price_list:
                List of objects used to calculate total price.
                Each label is rendered as a line item in the checkout dialog.
            is_test_payment:
                Whether this is a test payment.
                Once set to true, the charge will be a dummy charge.
    """

    def __init__(self,
                 currency: str,
                 payment_type: PaymentType,
                 merchant_name: str,
                 requested_user_info: list,
                 price_list: List[PriceList],
                 is_test_payment: Optional[bool]=None):
        self.syntax = {
            'currency': currency,
            'payment_type': payment_type,
            'is_test_payment': is_test_payment,
            'merchant_name': merchant_name,
            'requested_user_info': requested_user_info,
            'price_list': price_list
        }


class BuyButton(Button):
    """ The buy button begins the in-conversation payments flow.
        When tapped, the button opens a checkout dialog, where the message
        recipient may choose their payment method, shipping address,
        and other details.
        This makes it possible for you to offer products in-conversation
        that a message recipient can purchase from start to finish with
        their Facebook account.

        Args:
            title:
                Title of Buy Button. Must be "buy".
            payload:
                Developer defined metadata about the purchase.
            payment_summary:
                Fields used in the checkout dialog.

        The Buy Button is only available for US users.
        You will get the following error if you try to send to a user that
        is not in US.

        {
            "error":{
                "message": "(#200) The user is not eligible to receive
                            payment messages.",
            "type":"OAuthException",
            "code":200,
            "error_subcode":2018112,
            "fbtrace_id":"DdAqW91SO+K"
        }

        You can also use the User Profile API and check the is_payment_enabled
        field to see if a user is eligible for payment before hand.
    """
    type_ = 'payment'
    templates = [GenericTemplate, ListTemplate, MediaTemplate]

    def __init__(self,
                 title: str,
                 payload: str,
                 payment_summary: PaymentSummary
                 ):
        self.syntax = {
            'type': self.type_,
            'title': title,
            'payload': payload,
            'payment_summary': payment_summary
        }


class CallButton(Button):
    """ The call button dials a phone number when tapped.

        Args:
            title:
                Button title, 20 character limit.
            payload:
                Format must have "+" prefix followed by the country code,
                area code and local number. For example, +16505551234.
    """
    type_ = 'phone_number'
    templates = [GenericTemplate, ListTemplate, ButtonTemplate, MediaTemplate]

    def __init__(self,
                 title: str,
                 payload: str):
        self.syntax = {
            'type': self.type_,
            'title': title,
            'payload': payload
        }


class LogInButton(Button):
    """ The log in button is used in the account linking flow,
        which lets you link the message recipient's identity on Messenger
        with their account on your site by directing them to your
        web-based login flow for authentication.

        Args:
            url:
                Authentication callback URL. Must use HTTPS protocol.
    """
    type_ = 'account_link'
    templates = [GenericTemplate, ListTemplate, ButtonTemplate, MediaTemplate]

    def __init__(self,
                 url: str):
        self.syntax = {
            'type': self.type_,
            'url': url
        }


class LogOutButton(Button):
    """ The log out button is used in the account linking flow
        to unlink the message recipient's identity on Messenger
        with their account on your site.
    """
    type_ = 'account_unlink'
    templates = [GenericTemplate, ListTemplate, ButtonTemplate, MediaTemplate]

    def __init__(self):
        self.syntax = {
            'type': self.type_
        }


class GameMetadata(RequestConstructor):
    """ Parameters specific to Instant Games.

        Args:
            player_id:
                Player ID (Instant Game name-space) to play against.
            context_id:
                Context ID (Instant Game name-space) of the THREAD to play in.
    """

    def __init__(self,
                 player_id: Optional[str],
                 context_id: Optional[str]):
        self.syntax = {
            'player_id': player_id,
            'context_id': context_id
        }


class GamePlayButton(Button):
    """ The game play button launches an Instant Game that is
        associated with your Facebook Page.

        Args:
            title:
                Button title, e.g. "Play".
            payload:
                This data will be sent to the game.
            game_metadata:
                Parameters specific to Instant Games.
    """
    type_ = 'game_play'
    templates = [GenericTemplate, ListTemplate, ButtonTemplate, MediaTemplate]

    def __init__(self,
                 title: str,
                 payload: Optional[str]=None,
                 game_metadata: Optional[GameMetadata]=None):
        self.syntax = {
            'type': self.type_,
            'title': title,
            'payload': payload,
            'game_metadata': game_metadata
        }
