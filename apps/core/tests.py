from django.test import SimpleTestCase

from .templatetags.utils_filters import youtube_embed


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


class AyudaViewTests(SimpleTestCase):
    def test_ayuda_url_resolves(self):
        response = self.client.get('/ayuda/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/ayuda.html')

