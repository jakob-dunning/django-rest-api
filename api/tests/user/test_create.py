import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized

from api import models
from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_EMAIL: Final[str] = 'hansi@haxno.ul'
VALID_NAME: Final[str] = 'Johnny Bravo'


class CreateUserTestCase(TestCase):

    def test_create_user(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': VALID_EMAIL,
                'name': VALID_NAME,
            }),
            content_type=HttpHeaderContentType.JSON
        )
        response_body = json.loads(response.content)

        user = models.User.objects.get(pk=response_body['id'])

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(user.email, VALID_EMAIL)
        self.assertEqual(user.name, VALID_NAME)
        self.assertEqual(user.shopping_cart, None)

    def test_create_user_with_long_email_address_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': 'karl.friedrich.von.und.zu.boerne@mymotherfuckinglongurl.com',
                'name': VALID_NAME,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_user_with_empty_email_address_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': '',
                'name': VALID_NAME,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_user_with_long_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': VALID_EMAIL,
                'name': 'Karl-Heinz Eckart von Hirschhausen zu Thurn und Taxis Rothschild',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_user_with_empty_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
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
    def test_create_product_with_missing_attribute_returns_bad_request(self, user_data: dict[str, str]) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps(user_data),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/user/',
            json.dumps({
                'email': VALID_EMAIL,
                'name': VALID_NAME,
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
