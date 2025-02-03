import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase


class GetShoppingCartTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart.json']

    def test_get_shopping_cart(self) -> None:
        response: HttpResponse = self.client.get('/api/shopping-cart/7/')
        product_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(
            product_data,
            {
                'id': 7
            }
        )

    def test_get_shopping_cart_with_non_existing_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.get('/api/shopping-cart/99/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
