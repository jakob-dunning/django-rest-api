import json

from django.http import HttpResponse
from django.test import TestCase


class ListShoppingCartPositionTestCase(TestCase):
    fixtures: list[str] = ['user_with_shopping_cart.json', 'shopping_cart_position.json']

    def test_list_shopping_cart_positions(self) -> None:
        response: HttpResponse = self.client.get('/api/shopping_cart/7/shopping_cart_position/')
        product_data: list[dict[str, int]] = json.loads(response.content)

        self.assertEqual(len(product_data), 1)
        self.assertDictEqual(
            product_data[0],
            {
                'id': 23,
                'product': 5,
                'shopping_cart': 7,
                'amount': 9,
            }
        )
