import django

from rest_framework import test


class AuthenticatedApiTestCase(test.APITestCase):
    fixtures = ['player_alice']
    username, password = 'Alice', 'Alice'

    @classmethod
    def setUpClass(cls):
        django.setup()
        super().setUpClass()
        from django.contrib.auth import models as auth_models
        cls.user = auth_models.User.objects.get(username=cls.username)

    def setUp(self):
        self.client.login(username=self.username, password=self.password)
