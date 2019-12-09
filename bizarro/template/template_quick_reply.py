from bizarro.utility.tag import Tags
from bizarro.utility.util import Utility


class QuickReply():
    reference = "https://developers.facebook.com/docs/messenger-platform/reference/send-api/quick-replies/"

    def __init__(self, user_id: str):
        """
        :type user_id: str
        :param user_id: current user_id of the particular user from Facebook
        """
        self.user_id = user_id
        self.utility = Utility()

    def quick_reply(self, title: str, payload: list):
        """
        *attachment is not enabled at this moment.*
        This will generate a complete payload for the quick reply

        **Reference**: "https://developers.facebook.com/docs/messenger-platform/reference/send-api/quick-replies/"

        :type title: str
        :param title: Contains the title of the quick reply payload.
        :type payload: list
        :param payload: payload generated from quick_reply_payload_generator function.

        :returns: :dict
        """
        if type(payload) != list:
            return
        if not self.__quick_reply_payload_validation(payload):
            return

        if title is None or len(title) == 0:
            return
        message = {
            Tags.TAG_TEXT: title,
            Tags.TAG_QUICK_REPLIES: payload,
        }
        quick_reply_payload = self.utility.create_basic_recipient(
            self.user_id)
        quick_reply_payload[Tags.TAG_MESSAGE] = message
        return quick_reply_payload

    def __quick_reply_payload_validation(self, payload: list):
        """
        this function validate the quick reply payload before sending it back to calling function.

        :type payload: list
        :param payload: payload to check if it pass the validation to be used as a payload for Quick Reply. **Maximum of 11 quick reply items are allowed**

        :returns: bool
        """
        error_name = "q_reply_payload_validation"
        if len(payload) > 11:
            # error - payload cannot have more than 11 items
            return False
        for items in payload:
            if Tags.TAG_CONTENT_TYPE in items:
                _content_type = items[Tags.TAG_CONTENT_TYPE]
                if _content_type == 'text':
                    _title = items[Tags.TAG_TITLE] if Tags.TAG_TITLE in items else None
                    _payload = items[Tags.TAG_PAYLOAD] if Tags.TAG_PAYLOAD in items else None
                    _image_url = items[Tags.TAG_IMAGE_URL] if Tags.TAG_IMAGE_URL in items else None

                    # check here title, payload and image_url
                    if _image_url is not None:
                        if len(_image_url) > 0:
                            if not Utility.url_validation(_image_url):
                                # url is not valid
                                return False
                    if _title is None and _image_url is None:
                        # error:
                        return False
                    if _image_url is None and _payload is None:
                        # error
                        return False
                else:
                    if Tags.TAG_IMAGE_URL in items:
                        _image_url = items[Tags.TAG_IMAGE_URL]
                        if len(_image_url) > 0:
                            if not Utility.url_validation(_image_url):
                                # url is not valid.
                                return False
            else:
                return False
        return True

    def quick_reply_create(self, content_type: str, title_text: str = '', payload: str = '', image_url: str = ''):
        """
        generates a single entry payload for quick reply. It makes it easier to generate payload for quick reply

        **Reference**: "https://developers.facebook.com/docs/messenger-platform/reference/send-api/quick-replies/"

        :type content_type: str
        :param content_type: content_type can be text, location, user_phone_number, user_email
        :type title_text: str
        :param title_text: The text to display on the quick reply button. **maximum of 11 quick replies are supported.** **Required** if content_type is 'text'. *20 characters limit*.
        :type payload: str
        :param payload: **Required if *content_type* is 'text'**. Custom data that will be sent back to you via the *messaging_postbacks webhook event*. **1000 characters limit**. *May set to an empty string if **image_url** is set.*
        :type image_url: str
        :param image_url: *Optional.* URL of image to display on the quick reply button for text quick replies. **Image should be a minimum of 24px x 24px.** Larger images will be automatically cropped and resized. **Required if title is an empty string.**

        :returns: :dict
        """
        error_name = 'quick_reply_create'
        if content_type == Tags.TAG_CONTENT_TYPE_TEXT:
            if len(payload) > 1000:
                # error - length of payload cannot exceed 1000 characters limit
                return {}
            if len(title_text) > 20:
                # generate soft warning message.
                pass  # this is a warning
            if title_text == '' and image_url == '':
                # generate error. both cannot be empty
                return {}
            if payload == '' and image_url == '':
                # generate error, both cannot be empty
                return {}
            if len(image_url) != 0:
                # if there is any value in image_url then it would be checked
                if not Utility.url_validation(image_url):
                    return {}
        return {
            Tags.TAG_CONTENT_TYPE: content_type,
            Tags.TAG_TITLE: title_text,
            Tags.TAG_PAYLOAD: payload,
            Tags.TAG_IMAGE_URL: image_url,
        }
