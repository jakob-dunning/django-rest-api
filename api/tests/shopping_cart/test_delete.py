from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api.models import ShoppingCart, User
from api.enums.HttpHeaderContentType import HttpHeaderContentType


class DeleteShoppingCartTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart.json']
    FIXTURE_SHOPPING_CART_ID: Final[int] = 7

    def test_delete_shopping_cart(self) -> None:
        response: HttpResponse = self.client.delete(
            f'/api/shopping-cart/{self.FIXTURE_SHOPPING_CART_ID}/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(ShoppingCart.objects.filter(pk=self.FIXTURE_SHOPPING_CART_ID).exists(), False)
        self.assertEqual(User.objects.get(pk=17).shopping_cart, None)

    def test_delete_shopping_cart_with_wrong_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.delete(
            '/api/shopping-cart/999/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
