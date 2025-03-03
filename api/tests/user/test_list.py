import json

from django.http import HttpResponse
from django.test import TestCase


class ListUsersTestCase(TestCase):
    fixtures: list[str] = ['user.json']

    def test_list_users(self) -> None:
        response: HttpResponse = self.client.get('/api/user/')
        product_data: list[dict[str, int]] = json.loads(response.content)

        self.assertEqual(len(product_data), 1)
        self.assertDictEqual(
            product_data[0],
            {
                'id': 3,
                'email': 'manfred@lkwpeter.com',
                'name': 'Manni Görgens',
                'shopping_cart': None,
            }
        )
