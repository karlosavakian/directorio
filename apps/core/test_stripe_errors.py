from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
import stripe

class StripeErrorHandlingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client = Client(enforce_csrf_checks=True)
        self.client.login(username="user", password="pass")
        self.client.get("/")
        self.csrftoken = self.client.cookies.get("csrftoken").value

    @override_settings(STRIPE_SECRET_KEY="sk_test")
    def test_create_payment_intent_handles_error(self):
        url = reverse("create_payment_intent")
        with patch("stripe.PaymentIntent.create", side_effect=stripe.error.StripeError("boom")):
            response = self.client.post(
                url,
                {"plan": "plata"},
                HTTP_X_CSRFTOKEN=self.csrftoken,
            )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    @override_settings(STRIPE_SECRET_KEY="sk_test")
    def test_create_checkout_session_handles_error(self):
        url = reverse("create_checkout_session")
        with patch("stripe.checkout.Session.create", side_effect=stripe.error.StripeError("boom")):
            response = self.client.post(
                url,
                {"plan": "plata"},
                HTTP_X_CSRFTOKEN=self.csrftoken,
            )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    @override_settings(STRIPE_SECRET_KEY="sk_test")
    def test_create_payment_intent_masks_api_key_on_auth_error(self):
        url = reverse("create_payment_intent")
        with patch(
            "stripe.PaymentIntent.create",
            side_effect=stripe.error.AuthenticationError("Invalid API Key provided: pk_test"),
        ):
            response = self.client.post(
                url,
                {"plan": "plata"},
                HTTP_X_CSRFTOKEN=self.csrftoken,
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("error"), "Invalid Stripe API key")

    @override_settings(STRIPE_SECRET_KEY="sk_test")
    def test_create_checkout_session_masks_api_key_on_auth_error(self):
        url = reverse("create_checkout_session")
        with patch(
            "stripe.checkout.Session.create",
            side_effect=stripe.error.AuthenticationError("Invalid API Key provided: pk_test"),
        ):
            response = self.client.post(
                url,
                {"plan": "plata"},
                HTTP_X_CSRFTOKEN=self.csrftoken,
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("error"), "Invalid Stripe API key")
