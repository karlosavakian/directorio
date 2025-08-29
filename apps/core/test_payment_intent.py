import json
from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse
import stripe


class PaymentIntentTests(TestCase):
    @patch("apps.core.views.public.get_stripe")
    def test_create_payment_intent_success(self, mock_get_stripe):
        mock_stripe = Mock()
        mock_get_stripe.return_value = mock_stripe
        mock_stripe.PaymentIntent.create.return_value = Mock(client_secret="cs_test")

        response = self.client.post(
            reverse("create_payment_intent"),
            data=json.dumps({"plan": "plata"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"clientSecret": "cs_test"})
        mock_stripe.PaymentIntent.create.assert_called_once_with(
            amount=900,
            currency="eur",
            payment_method_types=["card"],
            description="Registro Pro - Plan plata",
            metadata={"plan": "plata", "user_id": None},
        )

    @patch("apps.core.views.public.get_stripe")
    def test_create_payment_intent_error(self, mock_get_stripe):
        mock_stripe = Mock()
        mock_get_stripe.return_value = mock_stripe
        mock_stripe.PaymentIntent.create.side_effect = stripe.error.StripeError("fail")

        response = self.client.post(
            reverse("create_payment_intent"),
            data=json.dumps({"plan": "plata"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
