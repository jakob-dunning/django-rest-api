import json
from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from parameterized import parameterized
from typing_extensions import Final

from api import models
from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_MANUFACTURER: Final[str] = 'Samsung'
VALID_MODEL: Final[str] = 'Galaxy S10'
VALID_PRICE: Final[int] = 39900
VALID_CATEGORY: Final[str] = 'Smartphone'


class CreateProductTestCase(TestCase):

    def test_create_product(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': VALID_CATEGORY
            }),
            content_type=HttpHeaderContentType.JSON
        )
        response_body = json.loads(response.content)

        product = models.Product.objects.get(pk=response_body['id'])

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(product.manufacturer, VALID_MANUFACTURER)
        self.assertEqual(product.model, VALID_MODEL)
        self.assertEqual(product.price, VALID_PRICE)
        self.assertEqual(product.category, VALID_CATEGORY)

    def test_create_product_with_long_manufacturer_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': 'International Business Machines Corporation',
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_empty_manufacturer_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': '',
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_long_model_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': 'Microsoft Windows Vista Ultimate UPGRADE Limited Numbered Signature Blockchain Artifical Intelligence Edition',
                'price': VALID_PRICE,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_empty_model_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': '',
                'price': VALID_PRICE,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_negative_price_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': -5,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_too_high_price_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': 5000000,
                'category': VALID_CATEGORY,
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_long_category_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': 'Blockchain Artificial Intelligence Cloud Crypto Software',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_product_with_empty_category_name_returns_bad_request(self) -> None:
        response: HttpResponse = self.client.post(
            '/api/product/',
            json.dumps({
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'price': VALID_PRICE,
                'category': '',
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @parameterized.expand([
        [{
            'model': VALID_MODEL,
            'price': VALID_PRICE,
            'category': VALID_CATEGORY,
        }],
        [{
            'manufacturer': VALID_MANUFACTURER,
            'price': VALID_PRICE,
            'category': VALID_CATEGORY,
        }],
        [{
            'manufacturer': VALID_MANUFACTURER,
            'model': VALID_MODEL,
            'category': VALID_CATEGORY,
        }],
        [{
            'manufacturer': VALID_MANUFACTURER,
            'model': VALID_MODEL,
            'price': VALID_PRICE
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
                'manufacturer': VALID_MANUFACTURER,
                'model': VALID_MODEL,
                'category': VALID_CATEGORY,
                'price': VALID_PRICE,
                'unknown_field': 'xyz'
            }),
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
