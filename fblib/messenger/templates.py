from decimal import Decimal
from typing import Optional, List, Union

from fblib.messenger.common import (
    Button,
    Template,
    RequestConstructor,
    Recipient,
)


class DefaultAction(RequestConstructor):
    """ The default action executed when the template is tapped.
        Accepts the same properties as URL button, except title.

        Args:
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

    def __init__(self,
                 url: str,
                 webview_height_ratio: Optional[str]=None,
                 messenger_extensions: Optional[bool]=None,
                 fallback_url: Optional[str]=None,
                 webview_share_button: Optional[str]=None):
        self.syntax = {
            'type': self.type_,
            'url': url,
            'webview_height_ratio': webview_height_ratio,
            'messenger_extensions': messenger_extensions,
            'fallback_url': fallback_url,
            'webview_share_button': webview_share_button,
        }


class GenericElement(RequestConstructor):
    """ The generic element.

        Args:
            title:
                The title to display in the template. 80 character limit.
            subtitle:
                The subtitle to display in the template. 80 character limit.
            image_url:
                The URL of the image to display in the template.
            default_action:
                The default action executed when the template is tapped.
            buttons:
                An array of buttons to append to the template.
                A maximum of 3 buttons per element is supported.
    """
    def __init__(self,
                 title: str,
                 subtitle: Optional[str]=None,
                 image_url: Optional[str]=None,
                 default_action: Optional[DefaultAction]=None,
                 buttons: Optional[List[Button]]=None
                 ):
        self.syntax = {
            'title': title,
            'image_url': image_url,
            'subtitle': subtitle,
            'default_action': default_action,
            'buttons': buttons
        }


class GenericTemplate(Template):
    """ The generic template is a simple structured message
        that includes a title, subtitle, image, and up to three buttons.
        You may also specify a default_action object that sets a URL that
        will be opened in the Messenger webview when the template is tapped.

        Args:
            recipient:
                Description of the message recipient.
            elements:
                The generic template supports a maximum
                of 10 elements per message.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/template/generic

        Implementation:
        https://developers.facebook.com/docs/messenger-platform/send-messages/template/generic
    """
    template_type = 'generic'

    def __init__(self,
                 recipient: Recipient,
                 elements: Union[List[GenericElement],
                                 List['GenericTemplate']]):
        self.payload = {
            'template_type': self.template_type,
            'elements': elements
        }
        super().__init__(recipient=recipient, payload=self.payload)


class ListTemplate(Template):
    """ The list template allows you to send a structured message
        with a set of items rendered vertically.

        Args:
            recipient:
                Description of the message recipient.
            elements:
                The generic template supports a maximum
                of 10 elements per message.
            top_element_style
                Sets the format of the first list items.
                Messenger web client currently only renders compact.
                `compact` Renders a plain list item.
                `large` Renders the first list item as a cover item.
            buttons:
                Button to display at the bottom of the list.
                Maximum of 1 button is supported.
            elements:
                Array of objects that describe items in the list.
                Minimum of 2 elements required.
                Maximum of 4 elements is supported.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/template/list

        Implementation:
        https://developers.facebook.com/docs/messenger-platform/send-messages/template/list
    """
    template_type = 'list'

    def __init__(self,
                 recipient: Recipient,
                 elements: List[GenericElement],
                 top_element_style: Optional[str]=None,
                 buttons: Optional[List[Button]]=None
                 ):
        self.payload = {
            'template_type': self.template_type,
            'top_element_style': top_element_style,
            'buttons': buttons,
            'elements': elements
        }
        super().__init__(recipient=recipient, payload=self.payload)


class ButtonTemplate(Template):
    """ The button template allows you to send a structured message
        that includes text and buttons.

        Args:
            recipient:
                Description of the message recipient.
            text:
                UTF-8-encoded text of up to 640 characters.
                Text will appear above the buttons.
            buttons:
                List of 1-3 buttons that appear as call-to-actions.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/template/button

        Implementation:
        https://developers.facebook.com/docs/messenger-platform/send-messages/template/button
    """
    template_type = 'button'

    def __init__(self,
                 recipient: Recipient,
                 text: str,
                 buttons: Optional[List[Button]] = None
                 ):
        self.payload = {
            'template_type': self.template_type,
            'text': text,
            'buttons': buttons
        }
        super().__init__(recipient=recipient, payload=self.payload)


class OpenGraphTemplate(Template):
    """ The Open Graph template allows you to send a structured message
        with an Open Graph URL, plus an optional button.
        Currently, only sharing songs is supported.
        The song will appear in a bubble that allows the message recipient
        to see album art and preview the song.

        To share an Open Graph template from the Messenger webview with
        beginShareFlow(), you must first call getSupportedFeatures()
        and verify the `sharing_open_graph` feature is available.

        Args:
            recipient:
                Description of the message recipient.
            url:
                String to display as the title of the list item.
                80 character limit.
                May be truncated if the title spans too many lines.
            buttons:
                An array of buttons to append to the template.
                Open graph templates sent via beginShareFlow()
                support a maximum of 1 button with `"type": "web_url".
                Open graph templates sent via the Send API
                support a maximum of 3 buttons of any type.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/template/open-graph

        Implementation:
        https://developers.facebook.com/docs/messenger-platform/send-messages/template/open-graph
    """
    template_type = 'open_graph'

    def __init__(self,
                 recipient: Recipient,
                 url: str,
                 buttons: List[Button] = None
                 ):
        self.payload = {
            'template_type': self.template_type,
            'url': url,
            'buttons': buttons
        }
        super().__init__(recipient=recipient, payload=self.payload)


class ReceiptElements(RequestConstructor):
    """ Receipt elements.

        Args:
            title:
                The name to display for the item.
            subtitle:
                The subtitle for the item, usually a brief item description.
            quantity:
                The quantity of the item purchased.
            price:
                The price of the item. For free items, '0' is allowed.
            currency:
                The currency of the item price.
            image_url:
                The URL of an image to be displayed with the item.
    """
    def __init__(self,
                 title: str,
                 price: Decimal,
                 subtitle: Optional[str],
                 quantity: Optional[int],
                 currency: Optional[str],
                 image_url: Optional[str]):
        self.syntax = {
            'title': title,
            'subtitle': subtitle,
            'quantity': quantity,
            'price': price,
            'currency': currency,
            'image_url': image_url
        }


class Summary(RequestConstructor):
    """ The property values of the summary object
        should be valid, well-formatted decimal numbers,
        using '.' (dot) as the decimal separator.
        Please note that most currencies only accept up to 2 decimal places.

        Args:
            total_cost:
                The total cost of the order,
                including sub-total, shipping, and tax.
            subtotal:
                The sub-total of the order.
            shipping_cost:
                The shipping cost of the order.
            total_tax:
                The tax of the order.
    """
    def __init__(self,
                 total_cost: Decimal,
                 subtotal: Optional[Decimal],
                 shipping_cost: Optional[Decimal],
                 total_tax: Optional[Decimal]):
        self.syntax = {
            'total_cost': total_cost,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'total_tax': total_tax
        }


class Address(RequestConstructor):
    """ Address

        Args:
            street_1:
                The street address, line 1.
            city:
                The city name of the address.
            postal_code:
                The postal code of the address.
            state:
                The state abbreviation for U.S. addresses,
                or the region/province for non-U.S. addresses.
            country:
                The two-letter country abbreviation of the address.
            street_2:
                The street address, line 2.
    """
    def __init__(self,
                 street_1: str,
                 city: str,
                 postal_code: str,
                 state: str,
                 country: str,
                 street_2: Optional[str]=None):
        self.syntax = {
            'street_1': street_1,
            'city': city,
            'postal_code': postal_code,
            'state': state,
            'country': country,
            'street_2': street_2
        }


class Adjustment(RequestConstructor):
    """ Adjustment

        Args:
            name:
                Name of the adjustment.
            amount:
                The amount of the adjustment.
    """
    def __init__(self, name: str, amount: Decimal):
        self.syntax = {
            'name': name,
            'amount': amount
        }


class ReceiptTemplate(Template):
    """ The receipt template allows you to send an order confirmation
        as a structured message.

        Args:
            recipient:
                Description of the message recipient.
            sharable:
                Set to true to enable the native share button in Messenger
                for the template message. Defaults to false.
            recipient_name:
                The recipient's name.
            merchant_name:
                The merchant's name. If present this is shown as logo text.
            order_number:
                The order number. Must be unique.
            currency:
                The currency of the payment.
            payment_method:
                The payment method used.
                Providing enough information for the customer to decipher which
                payment method and account they used is recommended.
                This can be a custom string, such as, "Visa 1234".
            timestamp:
                Timestamp of the order in seconds.
            elements:
                Array of a maximum of 100 element objects that describe items in the order. Sort order of the elements is not guaranteed.
            address:
                The shipping address of the order.
            summary:
                The payment summary.
            adjustments:
                An array of payment objects that describe payment adjustments,
                such as discounts.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/template/receipt

        Implementation:
        https://developers.facebook.com/docs/messenger-platform/send-messages/template/receipt
    """
    template_type = 'receipt'

    def __init__(self,
                 recipient: Recipient,
                 recipient_name: str,
                 order_number: str,
                 currency: str,
                 payment_method: str,
                 summary: Summary,
                 sharable: Optional[bool]=None,
                 merchant_name: Optional[str]=None,
                 timestamp: Optional[str]=None,
                 elements: Optional[ReceiptElements]=None,
                 address: Optional[Address]=None,
                 adjustments: Optional[List[Adjustment]]=None):
        self.payload = {
            'template_type': self.template_type,
            'sharable': sharable,
            'recipient_name': recipient_name,
            'merchant_name': merchant_name,
            'order_number': order_number,
            'currency': currency,
            'payment_method': payment_method,
            'timestamp': timestamp,
            'elements': elements,
            'address': address,
            'summary': summary,
            'adjustments': adjustments
        }
        super().__init__(recipient=recipient, payload=self.payload)


class AuxiliaryField(RequestConstructor):
    """ Flexible information to display in the auxiliary and secondary section.

        Args:
            label:
                Label for the additional field.
            value:
                Value for the additional field.
    """
    def __init__(self, label: str, value: str):
        self.syntax = {
            'label': label,
            'value': value,
        }


class FlightSchedule(RequestConstructor):
    """ Schedule for the flight.

        Args:
            boarding_time:
                Boarding time in departure airport timezone.
                Must be in the ISO 8601-based format YYYY-MM-DDThh:mm
                (e.g. 2015-09-26T10:30).
            departure_time:
                Departure time in departure airport timezone.
                Must be in the ISO 8601-based format YYYY-MM-DDThh:mm
                (e.g. 2015-09-26T10:30).
            arrival_time:
                Arrival time in arrival airport timezone.
                Must be in the ISO 8601-based format YYYY-MM-DDThh:mm
                (e.g. 2015-09-26T10:30).
    """
    def __init__(self,
                 departure_time: str,
                 boarding_time: Optional[str],
                 arrival_time: Optional[str]):
        self.syntax = {
            'boarding_time': boarding_time,
            'departure_time': departure_time,
            'arrival_time': arrival_time
        }


class DepartureAirport(RequestConstructor):
    """ Departure airport.

        Args:
            airport_code:
                Airport code of the departure airport.
            city:
                Departure city of the flight.
            terminal:
                Terminal of the departing flight.
            gate:
                Gate for the departing flight.
    """
    def __init__(self,
                 airport_code: str,
                 city: str,
                 terminal: str,
                 gate: str):
        self.syntax = {
            'airport_code': airport_code,
            'city': city,
            'terminal': terminal,
            'gate': gate
        }


class ArrivalAirport(RequestConstructor):
    """ Departure airport.

        Args:
            airport_code:
                Airport code of the departure airport.
            city:
                Departure city of the flight.
    """
    def __init__(self,
                 airport_code: str,
                 city: str):
        self.syntax = {
            'airport_code': airport_code,
            'city': city
        }


class FlightInfo(RequestConstructor):
    """ Information about the flight.

        Args:
            flight_number:
                Flight number.
            departure_airport:
                Departure airport.
            arrival_airport:
                Arrival airport.
            flight_schedule:
                Schedule for the flight.
    """
    def __init__(self,
                 flight_number: str,
                 departure_airport: DepartureAirport,
                 arrival_airport: ArrivalAirport,
                 flight_schedule: FlightSchedule):
        self.syntax = {
            'flight_number': flight_number,
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport,
            'flight_schedule': flight_schedule
        }


class BoardingPass(RequestConstructor):
    """ Boarding passes for passengers.

        Args:
            passenger_name:
                Flight number
            pnr_number:
                Passenger name record number (Booking Number)
            travel_class:
                Travel class.
            seat:
                Seat number for passenger.
            auxiliary_fields:
                Flexible information to display in the auxiliary section.
            secondary_fields:
                Flexible information to display in the secondary section.
            logo_image_url:
                URL for the logo image.
            header_image_url:
                URL for the header image.
            header_text_field:
                Text for the header field.
            qr_code:
                Aztec or QR code. Not available if barcode_image_urlis used.
            barcode_image_url:
                URL of the barcode image. Not available if qr_code is used.
            above_bar_code_image_url:
                URL of thin image above the barcode.
            flight_info:
                Information about the flight. See flight_info.
    """
    def __init__(self,
                 passenger_name: str,
                 pnr_number: str,
                 logo_image_url: str,
                 qr_code: str,
                 barcode_image_url: str,
                 above_bar_code_image_url: str,
                 flight_info: FlightInfo,
                 travel_class: Optional[str]=None,
                 seat: Optional[str]=None,
                 auxiliary_fields: Optional[List[AuxiliaryField]]=None,
                 secondary_fields: Optional[List[AuxiliaryField]]=None,
                 header_image_url: Optional[str]=None,
                 header_text_field: Optional[str]=None
                 ):

        self.syntax = {
            'passenger_name': passenger_name,
            'pnr_number': pnr_number,
            'logo_image_url': logo_image_url,
            'qr_code': qr_code,
            'barcode_image_url': barcode_image_url,
            'above_bar_code_image_url': above_bar_code_image_url,
            'flight_info': flight_info,
            'travel_class': travel_class,
            'seat': seat,
            'auxiliary_fields': auxiliary_fields,
            'secondary_fields': secondary_fields,
            'header_image_url': header_image_url,
            'header_text_field': header_text_field
        }


class AirlineBoardingPassTemplate(Template):
    """ The airline boarding pass template allows you to send a structured
        message that contains boarding passes for one or more flights,
        for one or more passengers.

        Args:
            recipient:
                Description of the message recipient.
            intro_message:
                Introduction message
            locale:
                Two-letter language region code.
                Must be a two-letter ISO 639-1 language code and a
                ISO 3166-1 alpha-2 region code separated by an underscore.
                Used to translate field labels (e.g. en_US).
            theme_color:
                Background color of the attachment
                Must be a RGB hexadecimal string.
                Defaults to #009ddc.
            boarding_pass:
                Boarding passes for passengers.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/template/airline-boarding-pass

        Implementation:
        https://developers.facebook.com/docs/messenger-platform/send-messages/template/airline
    """
    template_type = 'airline_boardingpass'

    def __init__(self,
                 recipient: Recipient,
                 intro_message: str,
                 locale: str,
                 boarding_pass: List[BoardingPass],
                 theme_color: Optional[str]=None
                 ):
        self.payload = {
            'template_type': self.template_type,
            'intro_message': intro_message,
            'locale': locale,
            'theme_color': theme_color,
            'boarding_pass': boarding_pass,
        }
        super().__init__(recipient=recipient, payload=self.payload)


class AirlineCheckinReminderTemplate(Template):
    """ The airline check-in reminder template allows you to send a structured
        message that contains a check-in reminder with flight information.

        Args:
            recipient:
                Description of the message recipient.
            intro_message:
                Introduction message
            locale:
                Two-letter language region code.
                Must be a two-letter ISO 639-1 language code and a
                ISO 3166-1 alpha-2 region code separated by an underscore.
                Used to translate field labels (e.g. en_US).
            pnr_number:
                The Passenger Name Record number (Booking Number).
            checkin_url:
                The URL where the customer can check in for their flight.
            flight_info:
                The flight number, departure airport, arrival airport,
                and schedule information for the flight.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/template/airline-checkin

        Implementation:
        https://developers.facebook.com/docs/messenger-platform/send-messages/template/airline
    """
    template_type = 'airline_checkin'

    def __init__(self,
                 recipient: Recipient,
                 intro_message: str,
                 locale: str,
                 checkin_url: str,
                 flight_info: FlightInfo,
                 pnr_number: Optional[str] = None,
                 ):
        self.payload = {
            'template_type': self.template_type,
            'intro_message': intro_message,
            'locale': locale,
            'checkin_url': checkin_url,
            'flight_info': flight_info,
            'pnr_number': pnr_number,
        }
        super().__init__(recipient=recipient, payload=self.payload)


class AirlineItineraryUpdateTemplate(Template):
    """ The airline itinerary template allows you to send a structured message
        that contains a check-in reminder with flight information.

        Args:
            recipient:
                Description of the message recipient.
            template_type:
                Value must be airline_itinerary.
            intro_message:
                Introduction message.
            locale:
                Two-letter language region code.
                Must be a two-letter ISO 639-1 language code and a
                ISO 3166-1 alpha-2 region code separated by an underscore.
                Used to translate field labels (e.g. en_US).
            theme_color:
                Background color of the attachment.
                Must be a RGB hexadecimal string.
                Defaults to #009ddc.
            pnr_number:
                Passenger name record number (Booking Number).
            passenger_info:
                Information about a passenger.
            flight_info:
                Information about a flight.
            passenger_segment_info:
                Information unique to passenger/segment pair.
            price_info:
                Itemization of the total price.
                Maximum of 4 items is supported.
            base_price:
                Base price amount
            tax:
                Tax amount.
            total_price:
                Total price for the booking
            currency:
                Pricing currency. Must be a three digit ISO-4217-3 code.

        Reference:
        https://developers.facebook.com/docs/messenger-platform/reference/template/airline-itinerary

        Implementation:
        https://developers.facebook.com/docs/messenger-platform/send-messages/template/airline
    """
    template_type = 'airline_itinerary'

    def __init__(self,
                 recipient: Recipient,
                 intro_message: str,
                 locale: str,
                 ,
                 theme_color: Optional[str] = None
                 ):
        self.payload = {
            'template_type': self.template_type,
            'intro_message': intro_message,
            'locale': locale,
            'theme_color': theme_color,
        }
        super().__init__(recipient=recipient, payload=self.payload)


class AirlineFlightUpdateTemplate:
    """"""


class MediaTemplate:
    """"""
