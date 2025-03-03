import json
from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_AMOUNT: Final[int] = 8
SHOPPING_CART_POSITION_FIXTURE_ID: Final[int] = 23
SHOPPING_CART_POSITION_FIXTURE_PRODUCT_ID: Final[int] = 5
SHOPPING_CART_POSITION_FIXTURE_SHOPPING_CART_ID: Final[int] = 7


class UpdateShoppingCartPositionTestCase(TestCase):
    fixtures: list[str] = ['product.json', 'user_with_shopping_cart.json', 'shopping_cart_position.json']

    def test_update_shopping_cart_position(self) -> None:
        new_shopping_cart_position_data: dict[str, str | int] = {
            'amount': 3,
        }
        response = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps(new_shopping_cart_position_data)
        )
        actual_product_data: dict[str, int] = json.loads(response.content)

        self.assertDictEqual(
            new_shopping_cart_position_data | {
                'id': SHOPPING_CART_POSITION_FIXTURE_ID,
                'product': SHOPPING_CART_POSITION_FIXTURE_PRODUCT_ID,
                'shopping_cart': SHOPPING_CART_POSITION_FIXTURE_SHOPPING_CART_ID
            },
            actual_product_data
        )

    def test_update_shopping_cart_position_with_non_positive_amount_returns_bad_request(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps({
                'amount': -7
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_shopping_cart_position_with_too_large_amount_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps({
                'amount': 14000
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_shopping_cart_position_with_missing_amount_returns_bad_request(self, ) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps({}),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_update_shopping_cart_position_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.put(
            f'/api/shopping-cart-position/{SHOPPING_CART_POSITION_FIXTURE_ID}/',
            json.dumps({
                'amount': VALID_AMOUNT,
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
