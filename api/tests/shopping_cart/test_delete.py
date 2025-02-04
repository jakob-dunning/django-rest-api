from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api import models
from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_SHOPPING_CART_ID: Final[int] = 7


class DeleteShoppingCartTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart.json']

    def test_delete_shopping_cart(self) -> None:
        response: HttpResponse = self.client.delete(
            f'/api/shopping-cart/{VALID_SHOPPING_CART_ID}/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(models.ShoppingCart.objects.filter(pk=VALID_SHOPPING_CART_ID).exists(), False)
        self.assertEqual(models.User.objects.get(pk=17).shopping_cart, None)

    def test_delete_shopping_cart_with_wrong_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.delete(
            '/api/shopping-cart/999/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
