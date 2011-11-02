import urllib
import time

from django import test
from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from botify import Botify

from mock import patch
from contextlib import nested

USER_AGENTS = (
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1) VoilaBot BETA 1.2 (support.voilabot@orange-ftgroup.com)',
    'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)',
    'msnbot/2.0b (+http://search.msn.com/msnbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
)


class BotifyTest(test.TestCase):
    def setUp(self):
        self.client = Client()

    def test_simple(self):
        response = self.client.get(reverse('simple'))

        self.assertEqual(response.status_code, 200)

    def test_simple_crawable(self):
        with patch.object(Botify, 'send_data') as mock_method:
            mock_method.return_value = True

            response = self.client.get(reverse('simple'), {}, **{
                'HTTP_USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'HTTP_HOST': 'http://example.test'
            })

            self.assertEqual(response.status_code, 200)

    def test_canonical(self):
        response = self.client.get(reverse('canonical'))

        self.assertEqual(response.status_code, 200)

    def test_tracker(self):
        response = self.client.get(reverse('tracker'))

        self.assertEqual(response.status_code, 200)

    def test_is_crawlable(self):
        for user_agent in USER_AGENTS:
            is_crawlable = Botify.is_crawlable(None, user_agent)
            self.assertTrue(bool(is_crawlable))

        self.assertFalse(Botify.is_crawlable('http://example.test', USER_AGENTS[0][0]))

    def test_format_data(self):
        user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        botify = Botify({
            'HTTP_HOST': 'http://example.test',
            'PATH_INFO': '/example',
            'HTTP_USER_AGENT': user_agent,
            'REMOTE_ADDR': '127.0.0.1'
        })

        bot = '<ip>%s</ip><ua>%s</ua>' % (botify.ip, botify.user_agent)

        with nested(
            patch.object(Botify, 'send_data'),
            patch.object(time, 'time')
        ) as (send_data_method, time_method):
            send_data_method.return_value = True
            current_time = 1319812537
            time_method.return_value = current_time

            botify.set_code(200)

            data = botify.record()

            self.assertEquals(data, '<?xml version="2.0"?><crawl><load>0</load><code>200</code><time>%(time)s</time><url>%(url)s</url><api_key>%(api_key)s</api_key><bot>%(bot_id)s</bot><id>%(client_id)s</id></crawl>' % {
                'time': current_time,
                'url': urllib.quote(botify.get_url()),
                'api_key': settings.BOTIFY_API_KEY,
                'client_id': settings.BOTIFY_CLIENT_ID,
                'bot_id': bot
            })

            botify.add_tracker('example')

            self.assertRaises(ValueError, botify.add_tracker, ({'test': 'test'}))

            data = botify.record()

            self.assertEquals(data, '<?xml version="2.0"?><crawl><load>0</load><code>200</code><time>%(time)s</time><url>%(url)s</url><api_key>%(api_key)s</api_key><bot>%(bot_id)s</bot><id>%(client_id)s</id><trackers><t>example</t></trackers></crawl>' % {
                'time': current_time,
                'url': urllib.quote(botify.get_url()),
                'api_key': settings.BOTIFY_API_KEY,
                'client_id': settings.BOTIFY_CLIENT_ID,
                'bot_id': bot
            })

            botify.canonical = 'http://example.test/home'

            data = botify.record()

            self.assertEquals(data, '<?xml version="2.0"?><crawl><load>0</load><code>200</code><time>%(time)s</time><url>%(url)s</url><api_key>%(api_key)s</api_key><bot>%(bot_id)s</bot><id>%(client_id)s</id><trackers><t>example</t></trackers><canonical>http%%3A//example.test/home</canonical></crawl>' % {
                'time': current_time,
                'url': urllib.quote(botify.get_url()),
                'api_key': settings.BOTIFY_API_KEY,
                'client_id': settings.BOTIFY_CLIENT_ID,
                'bot_id': bot,
            })
