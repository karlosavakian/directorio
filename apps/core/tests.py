from datetime import timedelta

from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone
from unittest.mock import MagicMock, patch

from apps.core.templatetags.utils_filters import message_day, youtube_embed


class YoutubeEmbedTests(SimpleTestCase):
    def test_embed_with_extra_params(self):
        text = 'Check this https://youtu.be/abc123?si=XYZ'
        html = youtube_embed(text)
        self.assertIn('iframe', html)
        self.assertIn('abc123', html)

    def test_no_match_returns_escaped(self):
        text = '<script>alert(1)</script>'
        html = youtube_embed(text)
        self.assertNotIn('iframe', html)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', html)


class AyudaViewTests(TestCase):
    def test_ayuda_url_resolves(self):
        response = self.client.get('/ayuda/')
        self.assertEqual(response.status_code, 200)


class MessageDayFilterTests(SimpleTestCase):
    def test_returns_hoy_for_today(self):
        now = timezone.now()
        self.assertEqual(message_day(now), 'Hoy')

    def test_returns_ayer_for_yesterday(self):
        yesterday = timezone.now() - timedelta(days=1)
        self.assertEqual(message_day(yesterday), 'Ayer')

    def test_returns_date_for_older(self):
        old_date = timezone.now() - timedelta(days=2)
        expected = timezone.localtime(old_date).date().strftime('%d/%m/%Y')
        self.assertEqual(message_day(old_date), expected)


class PaymentIntentTests(SimpleTestCase):
    @patch("apps.core.views.public.stripe.PaymentIntent.create")
    def test_create_payment_intent_returns_client_secret(self, mock_create):
        mock_create.return_value = MagicMock(client_secret="test_secret")
        response = self.client.post(reverse("create_payment_intent"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"clientSecret": "test_secret"})


class CheckoutRoutesTests(TestCase):
    def test_checkout_success_view(self):
        response = self.client.get(reverse("checkout_success"))
        self.assertEqual(response.status_code, 200)

    def test_checkout_cancel_view(self):
        response = self.client.get(reverse("checkout_cancel"))
        self.assertEqual(response.status_code, 200)

