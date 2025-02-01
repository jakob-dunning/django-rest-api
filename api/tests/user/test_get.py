import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase


class GetUserTestCase(TestCase):
    fixtures: list[str] = ['user.json']

    def test_get_user(self) -> None:
        response: HttpResponse = self.client.get('/api/user/3/')
        product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(
            product_data,
            {
                'id': 3,
                'email': 'manfred@lkwpeter.com',
                'name': 'Manni Görgens',
                'shopping_cart': None
            }
        )

    def test_get_user_with_non_existing_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.get('/api/user/99/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
