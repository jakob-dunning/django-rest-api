import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

SHOPPING_CART_POSITION_FIXTURE_ID: Final[int] = 23
SHOPPING_CART_POSITION_FIXTURE_PRODUCT_ID: Final[int] = 5
SHOPPING_CART_POSITION_FIXTURE_SHOPPING_CART_ID: Final[int] = 7
SHOPPING_CART_POSITION_FIXTURE_AMOUNT: Final[int] = 9
INVALID_SHOPPING_CART_POSITION_ID: Final[int] = 999


class GetShoppingCartPositionTestCase(TestCase):
    fixtures: list[str] = ['product.json', 'user_with_shopping_cart.json', 'shopping_cart_position.json']

    def test_get_shopping_cart_position(self) -> None:
        response: HttpResponse = self.client.get('/api/shopping-cart-position/23/')
        shopping_cart_position_data: dict[str, str | int] = json.loads(response.content)

        self.assertDictEqual(
            shopping_cart_position_data,
            {
                'id': SHOPPING_CART_POSITION_FIXTURE_ID,
                'product': SHOPPING_CART_POSITION_FIXTURE_PRODUCT_ID,
                'shopping_cart': SHOPPING_CART_POSITION_FIXTURE_SHOPPING_CART_ID,
                'amount': SHOPPING_CART_POSITION_FIXTURE_AMOUNT
            }
        )

    def test_get_product_with_non_existing_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.get(f'/api/shopping-cart-position/{INVALID_SHOPPING_CART_POSITION_ID}/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
