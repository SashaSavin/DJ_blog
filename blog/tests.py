from django.test import TestCase

# Create your tests here.


class TestPage(TestCase):
    def test_index_page(self):
       url = ''
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'base.html')