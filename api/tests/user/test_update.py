import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized

from api.enums.HttpHeaderContentType import HttpHeaderContentType


class UpdateUserTestCase(TestCase):
    fixtures: list[str] = ['user.json']
    FIXTURE_USER_ID: Final[int] = 3

    def test_update_user(self) -> None:
        new_user_data: dict[str, str | int] = {
            'email': 'pop@zisch.com',
            'name': 'For the win',
        }
        self.client.put(
            f'/api/user/{self.FIXTURE_USER_ID}/',
            json.dumps(new_user_data)
        )
        response: HttpResponse = self.client.get(f'/api/user/{self.FIXTURE_USER_ID}/')
        actual_user_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(new_user_data | {'id': self.FIXTURE_USER_ID, 'shopping_cart': None}, actual_user_data)

    def test_update_user_with_long_email_address_returns_bad_request(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{self.FIXTURE_USER_ID}/',
            json.dumps({
                'email': 'international.business.machines.corporation@godaddy.cx',
                'name': 'Karl Zeiss',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_user_with_empty_email_address_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{self.FIXTURE_USER_ID}/',
            json.dumps({
                'email': '',
                'name': 'Izi Going',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_user_with_long_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{self.FIXTURE_USER_ID}/',
            json.dumps({
                'email': 'john@microsoft.com',
                'name': 'Microsoft Windows Vista Ultimate UPGRADE Limited Numbered Signature Blockchain Artifical Intelligence Edition',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_user_with_empty_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{self.FIXTURE_USER_ID}/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': '',
                'price': 30000,
                'category': 'PC',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand([
        [{
            'email': 'john@bonham.com',
        }],
        [{
            'name': 'Ingo Teufel',
        }]
    ])
    def test_update_user_with_missing_attribute_returns_bad_request(self, user_data: dict[str, str]) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{self.FIXTURE_USER_ID}/',
            json.dumps(user_data),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_user_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/user/{self.FIXTURE_USER_ID}/',
            json.dumps({
                'email': 'jhagsd@fff.de',
                'name': 'haxxx maxxx',
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
