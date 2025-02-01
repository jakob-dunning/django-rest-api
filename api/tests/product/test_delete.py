from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api.models import Product
from api.enums.HttpHeaderContentType import HttpHeaderContentType


class DeleteProductTestCase(TestCase):
    fixtures: list[str] = ['product.json']
    FIXTURE_PRODUCT_ID: Final[int] = 5

    def test_delete_product(self) -> None:
        response: HttpResponse = self.client.delete(
            f'/api/product/{self.FIXTURE_PRODUCT_ID}/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Product.objects.filter(pk=self.FIXTURE_PRODUCT_ID).exists(), False)

    def test_delete_product_with_wrong_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.delete(
            '/api/product/999/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
