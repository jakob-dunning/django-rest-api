import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized

from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_USER_ID: Final[int] = 3
VALID_EMAIL: Final[str] = 'hastabasta@ingozaperoni.com'
VALID_NAME: Final[str] = 'Thomas Anders'


class UpdateUserTestCase(TestCase):
    fixtures: list[str] = ['user.json']

    def test_update_user(self) -> None:
        new_user_data: dict[str, str | int] = {
            'email': VALID_EMAIL,
            'name': VALID_NAME,
        }
        self.client.put(
            f'/api/user/{VALID_USER_ID}/',
            json.dumps(new_user_data)
        )
        response: HttpResponse = self.client.get(f'/api/user/{VALID_USER_ID}/')
        actual_user_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(new_user_data | {'id': VALID_USER_ID, 'shopping_cart': None}, actual_user_data)

    def test_update_user_with_long_email_address_returns_bad_request(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{VALID_USER_ID}/',
            json.dumps({
                'email': 'international.business.machines.corporation@godaddy.cx',
                'name': VALID_NAME,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_user_with_empty_email_address_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{VALID_USER_ID}/',
            json.dumps({
                'email': '',
                'name': VALID_NAME,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_user_with_too_long_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{VALID_USER_ID}/',
            json.dumps({
                'email': VALID_EMAIL,
                'name': 'Microsoft Windows Vista Ultimate UPGRADE Limited Numbered Signature Blockchain Artifical Intelligence Edition',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_user_with_empty_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{VALID_USER_ID}/',
            json.dumps({
                'email': VALID_EMAIL,
                'name': '',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand([
        [{
            'email': VALID_EMAIL,
        }],
        [{
            'name': VALID_NAME,
        }]
    ])
    def test_update_user_with_missing_attribute_returns_bad_request(self, user_data: dict[str, str]) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{VALID_USER_ID}/',
            json.dumps(user_data),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_user_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{VALID_USER_ID}/',
            json.dumps({
                'email': VALID_EMAIL,
                'name': VALID_NAME,
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
