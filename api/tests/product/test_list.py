import json

from django.http import HttpResponse
from django.test import TestCase


class ListProductTestCase(TestCase):
    fixtures: list[str] = ['products.json']

    def test_list_products(self) -> None:
        response: HttpResponse = self.client.get('/api/product/')
        product_data: list[dict[str, str | int]] = json.loads(response.content)

        self.assertEqual(len(product_data), 2)
        self.assertDictEqual(
            product_data[0],
            {
                'id': 3,
                'manufacturer': 'B&O',
                'model': 'Beovox 300',
                'price': 255000,
                'category': 'Speaker'
            }
        )
        self.assertDictEqual(
            product_data[1],
            {
                'id': 6,
                'manufacturer': 'Heinz',
                'model': 'Ketchup',
                'price': 400,
                'category': 'Condiment'
            }
        )
