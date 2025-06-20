from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.clubs.models import Club
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os


class Command(BaseCommand):
    help = 'Scrape club data from feboxeo.es and store it in the database.'

    def handle(self, *args, **options):
        url = 'https://feboxeo.es/donde-boxeo/'
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/119.0.0.0 Safari/537.36'
            )
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as exc:
            self.stderr.write(f'Error fetching {url}: {exc}')
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        clubs = soup.select('.club-list-item')
        for item in clubs:
            name_el = item.select_one('.club-name')
            if not name_el:
                continue
            name = name_el.get_text(strip=True)

            address_el = item.select_one('.club-address')
            email_el = item.select_one('a[href^=mailto]')
            logo_el = item.select_one('img')

            address = address_el.get_text(strip=True) if address_el else ''
            email = email_el['href'].replace('mailto:', '') if email_el else ''
            logo_url = None
            if logo_el and logo_el.get('src'):
                logo_url = urljoin(url, logo_el['src'])

            club, created = Club.objects.get_or_create(
                name=name,
                defaults={'address': address, 'email': email}
            )
            if not created:
                club.address = address
                club.email = email
                club.save(update_fields=['address', 'email'])

            if logo_url:
                try:
                    img_resp = requests.get(logo_url, headers=headers)
                    img_resp.raise_for_status()
                    club.logo.save(
                        os.path.basename(logo_url),
                        ContentFile(img_resp.content),
                        save=True
                    )
                except requests.RequestException:
                    self.stderr.write(f'Failed to download logo for {name}')

        self.stdout.write(self.style.SUCCESS('Scraping completado'))
