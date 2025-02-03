import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase


class GetShoppingCartPositionTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart_and_shopping_cart_position.json']

    def test_get_shopping_cart_position(self) -> None:
        response: HttpResponse = self.client.get('/api/shopping-cart-position/23/')
        shopping_cart_position_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(
            shopping_cart_position_data,
            {
                'id': 23,
                'product': 25,
                'shopping_cart': 9,
                'amount': 9
            }
        )

    def test_get_product_with_non_existing_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.get('/api/shopping-cart-position/99/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
