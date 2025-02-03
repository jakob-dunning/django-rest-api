from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api.models import Product
from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_SHOPPING_CART_POSITION_ID: Final[int] = 23

class DeleteShoppingCartPositionTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart_and_shopping_cart_position.json']

    def test_delete_shopping_cart_position(self) -> None:
        response: HttpResponse = self.client.delete(
            f'/api/shopping-cart-position/{VALID_SHOPPING_CART_POSITION_ID}/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Product.objects.filter(pk=VALID_SHOPPING_CART_POSITION_ID).exists(), False)

    def test_delete_product_with_wrong_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.delete(
            '/api/shopping-cart-position/999/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
