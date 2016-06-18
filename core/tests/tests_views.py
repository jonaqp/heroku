from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import resolve
from django.test import Client, TestCase

User = get_user_model()


class TestLoggedUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('user@test.net', 'secret')
        self.user.save()
        self.client.login(username='test_user', password='secret')

    def tearDown(self):
        self.user.delete()

    def test_new_view_test_addflow(self):
        response = resolve('/')
        self.assertEqual(response.func.func_name, auth_views.login.func_name)

    # def test_renders_template_addflow(self):
    #     url = reverse('rep-add-flow')
    #     response = self.request_factory.post(url)
    #     self.assertTemplateUsed(response, '/pariwana/recepcion/addflow')
    #
    # def test_logged_user_get_homepage(self):
    #     print(self.user)
    #     response = self.client.get(reverse('/'), follow=True)
    #     self.assertEqual(response.status_code, 200)

    # def test_logged_user_get_settings(self):
    #     response = self.client.get(reverse('/settings/'), follow=True)
    #     self.assertEqual(response.status_code, 200)
