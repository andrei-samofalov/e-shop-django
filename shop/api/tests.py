from django.test import TestCase


class AccessApiMiddlewareTest(TestCase):
    def test_requests_with_header_passes(self):
        response = self.client.get(
            '/api/catalog/',
            headers={'X-HERE-I-AM': 'hello'}
        )
        self.assertEqual(response.status_code, 200)

    def test_requests_without_header_dont_pass(self):
        response = self.client.get(
            '/api/catalog/'
        )
        self.assertEqual(response.status_code, 403)

