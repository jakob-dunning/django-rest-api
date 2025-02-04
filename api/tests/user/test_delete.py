from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api import models
from api.enums.HttpHeaderContentType import HttpHeaderContentType

VALID_USER_ID: Final[int] = 3


class DeleteUserTestCase(TestCase):
    fixtures: list[str] = ['user.json']

    def test_delete_user(self) -> None:
        response: HttpResponse = self.client.delete(
            f'/api/user/{VALID_USER_ID}/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(models.User.objects.filter(pk=VALID_USER_ID).exists(), False)

    def test_delete_product_with_wrong_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.delete(
            '/api/user/999/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
