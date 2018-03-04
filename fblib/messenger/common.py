from enum import Enum
from typing import List, Optional, Union


class RequestConstructor:
    """ Construct requests to Facebook Messenger API.
    """
    syntax = {}

    def build(self):
        """ Convert self.syntax to dict, removing None's.
        """
        params = {k: v for k, v in self.syntax.items() if v is not None}
        return params


class Recipient:
    """ Description of the message recipient.
        All requests must include one of id, phone_number, or user_ref.

        Args:
            id_:
                Either PSID, phone_number, or user_ref
                of the message recipient.
            phone_number:
                Phone number of the recipient with the format +1(212)555-2368.
                Your bot must be approved for Customer Matching
                to send messages this way.
            user_ref:
                user_ref from the checkbox plugin.
            name:
                Used only if phone_number is set.
                Specifies the person's name in the format:
                    {"first_name":"John", "last_name":"Doe"}
                Providing a name increases the odds of a successful match.
    """
    def __init__(self, id_: str, phone_number: str, user_ref: str, name: dict):
        self.syntax = {
            'id': id_,
            'phone_number': phone_number,
            'user_ref': user_ref,
            'name': name
        }


class MessagingType(Enum):
    """ The messaging_type property identifies the messaging type of the
        message being sent, and is a more explicit way to ensure bots are
        complying with policies for specific messaging types and respecting
        people's preferences.

        The following values for 'messaging_type' are supported:

        RESPONSE:
            Message is in response to a received message.
            This includes promotional and non-promotional messages sent inside
            the 24-hour standard messaging window or under the 24+1 policy.
            For example, use this tag to respond if a person asks for
            a reservation confirmation or an status update.

        UPDATE:
            Message is being sent proactively and is not in response to a
            received message. This includes promotional and non-promotional
            messages sent inside the the 24-hour standard messaging window or
            under the 24+1 policy.

        MESSAGE_TAG:
            Message is non-promotional and is being sent outside
            the 24-hour standard messaging window with a message tag.
            The message must match the allowed use case for the tag.
    """
    RESPONSE = 'RESPONSE'
    UPDATE = 'UPDATE'
    MESSAGE_TAG = 'MESSAGE_TAG'


class Payload(RequestConstructor):
    """ Payload for rich media message.

        Args:
            url:
                attachment from a URL
            file:
                TODO: add file uploading option
            attachment_id:
                To attach a saved asset to a message specify the attachment_id.
            is_reusable:
                Only attachments that were uploaded with the is_reusable
                property set to true can be sent to other message recipients.

        Description:
        https://developers.facebook.com/docs/messenger-platform/send-messages
    """
    def __init__(self,
                 url: Optional[str]=None,
                 file: Optional[str]=None,  # TODO: add file uploading option
                 attachment_id: Optional[str]=None,
                 is_reusable: Optional[bool]=None):
        self.syntax = {
            'url': url,
            'attachment_id': attachment_id,
            'is_reusable': is_reusable
        }


class Template(RequestConstructor):
    """ Description of the template.
    """


class Attachment(RequestConstructor):
    """ The following can be included in the attachment object:
        - Rich media messages including images, audios, videos, or files.
        - Templates including generic template, button template,
          receipt template, or list template.

        Vars:
            type:
                Type of attachment, may be image, audio, video, file or
                template.
            payload:
                Payload of attachment.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/send-api/
    """
    def __init__(self,
                 type_: str,
                 payload: Union[Payload, Template]):
        self.syntax = {
            'type': type_,
            'payload': payload
        }


class QuickReply(RequestConstructor):
    """ Quick Replies allow you to get message recipient input by sending
        buttons in a message. When a quick reply is tapped, the value of the
        button is sent in the conversation, and the Messenger Platform sends
        a messages event to you webhook.

        Args:
            content_type:
                Must be one of the following
                text: Sends a text button
                location: Sends a button to collect the recipient's location
                user_phone_number: Sends a button allowing recipient to send
                    the phone number associated with their account.
                user_email: Sends a button allowing recipient to send the email
                    associated with their account.
            title:
                Required if content_type is 'text'.
                The text to display on the quick reply button.
                20 character limit.
            payload:
                Required if content_type is 'text'.
                Custom data that will be sent back to you via the
                messaging_postbacks webhook event.
                1000 character limit.
            image_url:
                URL of image to display on the quick reply button for
                text quick replies. Image should be a minimum of 24px x 24px.
                Larger images will be automatically cropped and resized.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/send-api/quick-replies
    """
    def __init__(self,
                 content_type: str,
                 title: Optional[str]=None,
                 payload: Optional[str]=None,
                 image_url: Optional[str]=None):
        self.syntax = {
            'content_type': content_type,
            'title': title,
            'payload': payload,
            'image_url': image_url
        }


class Message(RequestConstructor):
    """ Message

        Args:
            text:
                Message text.
                Previews will not be shown for the URLs in this field.
                Use attachment instead.
                Must be UTF-8 and has a 2000 character limit.
                text or attachment must be set.
            attachment:
                Previews the URL.
                Used to send messages with media or Structured Messages.
                text or attachment must be set.
            quick_replies:
                Array of quick_reply to be sent with messages
            metadata:
                Custom string that is delivered as a message echo.
                1000 character limit.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/send-api/
    """
    def __init__(self,
                 text: Optional[str]=None,
                 attachment: Optional[Attachment]=None,
                 quick_replies: Optional[List[QuickReply]]=None,
                 metadata: Optional[str]=None):
        self.syntax = {
            'text': text,
            'attachment': attachment,
            'quick_replies': quick_replies,
            'metadata': metadata
        }


class MessageTag(Enum):
    """ Message tags give you the ability to send messages to a person outside
        of the normally allowed 24-hour window for a limited number of purposes
        that require continual notification or updates. This enables greater
        flexibility in how your bot interacts with people, as well as the types
        of experiences you can build on the Messenger Platform.

        Supported tags:
            COMMUNITY_ALERT:
                Notify the message recipient of emergency or utility alerts,
                or issue a safety check in your community.
            CONFIRMED_EVENT_REMINDER:
                Send the message recipient reminders of a scheduled event whic
                 a person is going to attend.
            NON_PROMOTIONAL_SUBSCRIPTION:
                Send non-promotional messages under the News, Productivity,
                and Personal Trackers categories described in the Messenger
                Platform's subscription messaging policy.
                You can apply for access to use this tag under the
                Page Settings > Messenger Platform.
            PAIRING_UPDATE:
                Notify the message recipient that a pairing has been identified
                based on a prior request.
            APPLICATION_UPDATE:
                Notify the message recipient of an update on the status of
                their application.
            ACCOUNT_UPDATE:
                Notify the message recipient of a change to their account
                settings.
            PAYMENT_UPDATE:
                Notify the message recipient of a payment update for
                an existing transaction.
            PERSONAL_FINANCE_UPDATE:
                Confirm a message recipient's financial activity.
            SHIPPING_UPDATE:
                Notify the message recipient of a change in shipping status
                for a product that has already been purchased.
            RESERVATION_UPDATE:
                Notify the message recipient of updates to an existing
                reservation.
            ISSUE_RESOLUTION:
                Notify the message recipient of an update to a customer service
                issue that was initiated in a Messenger conversation.
            APPOINTMENT_UPDATE:
                Notify the message recipient of a change to an existing
                appointment.
            GAME_EVENT:
                Notify the message recipient of a change in in-game user
                progression, global events, or a live sporting event.
            TRANSPORTATION_UPDATE:
                Notify the message recipient of updates to an existing
                transportation reservation.
            FEATURE_FUNCTIONALITY_UPDATE:
                Notify the message recipient of new features or functionality
                that become available in your bot.
            TICKET_UPDATE:
                Send the message recipient updates or reminders for an event
                for which a person already has a ticket.

            Reference:
            https://developers.facebook.com/docs/messenger-platform/send-messages/message-tags
    """
    COMMUNITY_ALERT = 'COMMUNITY_ALERT'
    CONFIRMED_EVENT_REMINDER = 'CONFIRMED_EVENT_REMINDER'
    NON_PROMOTIONAL_SUBSCRIPTION = 'NON_PROMOTIONAL_SUBSCRIPTION'
    PAIRING_UPDATE = 'PAIRING_UPDATE'
    APPLICATION_UPDATE = 'APPLICATION_UPDATE'
    ACCOUNT_UPDATE = 'ACCOUNT_UPDATE'
    PAYMENT_UPDATE = 'PAYMENT_UPDATE'
    PERSONAL_FINANCE_UPDATE = 'PERSONAL_FINANCE_UPDATE'
    SHIPPING_UPDATE = 'SHIPPING_UPDATE'
    RESERVATION_UPDATE = 'RESERVATION_UPDATE'
    ISSUE_RESOLUTION = 'ISSUE_RESOLUTION'
    APPOINTMENT_UPDATE = 'APPOINTMENT_UPDATE'
    GAME_EVENT = 'GAME_EVENT'
    TRANSPORTATION_UPDATE = 'TRANSPORTATION_UPDATE'
    FEATURE_FUNCTIONALITY_UPDATE = 'FEATURE_FUNCTIONALITY_UPDATE'
    TICKET_UPDATE = 'TICKET_UPDATE'


class Request(RequestConstructor):
    """ The body of the HTTP request in JSON format.

        Vars:
            messaging_type:
                The messaging type of the message being sent.
            recipient:
                Recipient object.
            message:
                Cannot be sent with sender_action.
            sender_action:
                Message state to display to the user:
                    typing_on: display the typing bubble
                    typing_off: remove the typing bubble
                    mark_seen: display the confirmation icon
                Cannot be sent with message.
                Must be sent as a separate request. When using sender_action,
                recipient should be the only other property set in the request.
            notification_type:
                Push notification type:
                    REGULAR: sound/vibration
                    SILENT_PUSH: on-screen notification only
                    NO_PUSH: no notification
                Defaults to REGULAR.
            tag:
                The message tag string.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/send-api/
    """
    def __init__(self,
                 messaging_type: MessagingType,
                 recipient: Recipient,
                 message: Optional[Message]=None,
                 sender_action: Optional[str]=None,
                 notification_type: Optional[str]=None,
                 tag: Optional[MessageTag]=None):
        self.syntax = {
            'messaging_type': messaging_type,
            'recipient': recipient,
            'message': message,
            'sender_action': sender_action,
            'notification_type': notification_type,
            'tag': tag
        }


class Button(RequestConstructor):
    """ Base class for all Facebook Messenger buttons.
        More information:

        https://developers.facebook.com/docs/messenger-platform/send-messages/buttons
    """
    type_: str = 'Button type'
    templates: List[Template] = []
