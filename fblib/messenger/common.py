from typing import List


class RequestConstructor:
    """ Construct requests to Facebook Messenger API.
    """


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


class Template(RequestConstructor):
    """ Description of the template.

        Args:
            recipient:
                Description of the message recipient.
            payload:
                payload of the template.
    """

    def __init__(self,
                 recipient: Recipient,
                 payload: dict):
        self.syntax = {
            'recipient': recipient,
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': payload
                }
            }
        }


class Button(RequestConstructor):
    """ Base class for all Facebook Messenger buttons.
        More information:

        https://developers.facebook.com/docs/messenger-platform/send-messages/buttons
    """
    type_: str = 'Button type'
    templates: List[Template] = []
