from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser, User
from asset.views import edit
from asset.models import Object


class EditTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

        # Create an object to test with
        Object.objects.create(name='laptop', friendly_name='Laptop', desc='A laptop',
                              active=True)

    def test_redirect_on_invalid_object(self):
        request = self.factory.get('/asset/edit/an_object')

        request.user = self.user

        response = edit(request, 'an_object')
        response.client = Client()
        self.assertRedirects(response, '/asset/create', status_code=302, target_status_code=200)

    def test_dont_redirect_on_valid_object(self):
        request = self.factory.get('/asset/edit/laptop')

        request.user = self.user

        response = edit(request, 'laptop')
        response.client = Client()
        self.assertEqual(response.status_code, 200)
