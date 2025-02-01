import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized

from api.models import Product
from api.enums.HttpHeaderContentType import HttpHeaderContentType


class CreateProductTestCase(TestCase):

    def test_create_product(self) -> None:
        manufacturer: str = 'Samsung'
        model: str = 'Galaxy S10'
        price: int = 39900
        category: str = 'Smartphone'

        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': manufacturer,
                'model': model,
                'price': price,
                'category': category
            }),
            content_type=HttpHeaderContentType.JSON
        )
        response_body = json.loads(response.content)

        product = Product.objects.get(pk=response_body['id'])

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(product.manufacturer, manufacturer)
        self.assertEqual(product.model, model)
        self.assertEqual(product.price, price)
        self.assertEqual(product.category, category)

    def test_create_product_with_long_manufacturer_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'International Business Machines Corporation',
                'model': 'PDP-11',
                'price': 30000,
                'category': 'PC',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_empty_manufacturer_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': '',
                'model': 'PDP-11',
                'price': 30000,
                'category': 'PC',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_long_model_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Microsoft Windows Vista Ultimate UPGRADE Limited Numbered Signature Blockchain Artifical Intelligence Edition',
                'price': 30000,
                'category': 'Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_empty_model_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': '',
                'price': 30000,
                'category': 'PC',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_negative_price_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Windows',
                'price': -5,
                'category': 'Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_high_price_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Windows',
                'price': 5000000,
                'category': 'Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_long_category_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Windows',
                'price': 30000,
                'category': 'Blockchain Artificial Intelligence Cloud Crypto Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_empty_category_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'Microsoft',
                'model': 'Windows',
                'price': 30000,
                'category': '',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand([
        [{
            'model': 'PDP-11',
            'price': 30000,
            'category': 'PC',
        }],
        [{
            'manufacturer': 'IBM',
            'price': 30000,
            'category': 'PC',
        }],
        [{
            'manufacturer': 'IBM',
            'model': 'PDP-11',
            'category': 'PC',
        }],
        [{
            'manufacturer': 'IBM',
            'model': 'PDP-11',
            'price': 30000
        }]
    ])
    def test_create_product_with_missing_attribute_returns_bad_request(self, product_data) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps(product_data),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_unknown_attribute_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'IBM',
                'model': 'PDP-11',
                'category': 'PC',
                'price': 999,
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
