import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

INVALID_USER_ID: Final[int] = 999
VALID_USER_ID: Final[int] = 3
VALID_EMAIL: Final[str] = 'manfred@lkwpeter.com'
VALID_NAME: Final[str] = 'Manni Görgens'


class GetUserTestCase(TestCase):
    fixtures: list[str] = ['user.json']

    def test_get_user(self) -> None:
        response: HttpResponse = self.client.get('/api/user/3/')
        product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(
            product_data,
            {
                'id': VALID_USER_ID,
                'email': VALID_EMAIL,
                'name': VALID_NAME,
                'shopping_cart': None
            }
        )

    def test_get_user_with_non_existing_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.get(f'/api/user/{INVALID_USER_ID}/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
