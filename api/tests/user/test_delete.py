from http import HTTPStatus
from typing import Final

from django.http import HttpResponse
from django.test import TestCase

from api.models import User
from api.enums.HttpHeaderContentType import HttpHeaderContentType


class DeleteUserTestCase(TestCase):
    fixtures: list[str] = ['user.json']
    FIXTURE_USER_ID: Final[int] = 3

    def test_delete_user(self) -> None:
        response: HttpResponse = self.client.delete(
            f'/api/user/{self.FIXTURE_USER_ID}/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(User.objects.filter(pk=self.FIXTURE_USER_ID).exists(), False)

    def test_delete_product_with_wrong_id_returns_not_found(self) -> None:
        response: HttpResponse = self.client.delete(
            '/api/user/999/',
            content_type=HttpHeaderContentType.JSON
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
