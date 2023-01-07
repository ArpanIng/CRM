from django.test import TestCase
from django.urls import reverse


class HomepageViewTestCase(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
