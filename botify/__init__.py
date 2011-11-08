# -*- coding: utf-8 -*-
import time
import urllib
from datetime import datetime
from socket import socket, SOCK_DGRAM, AF_INET

from django.conf import settings

class Botify(object):

    def __init__(self, meta):
        self.http_host = meta.get('HTTP_HOST', None)
        self.path_info = meta.get('PATH_INFO', None)
        self.user_agent = meta.get('HTTP_USER_AGENT', None)
        self.ip = meta.get('REMOTE_ADDR', None)
        self.time_init = datetime.now()
        self.trackers = []
        self.canonical = ''

    @staticmethod
    def is_crawlable(http_referer, user_agent):
        if (not user_agent or
            http_referer or
            (not len([key for key in ('bot', 'search', 'crawl',)
                      if key in user_agent.lower()]))):
            return False
        return True

    def add_tracker(self, trackers):
        if isinstance(trackers, list):
            self.trackers += trackers
        elif isinstance(trackers, str):
            self.trackers.append(trackers)
        else:
            raise ValueError("add_tracker() argument must be a string or a list")

    def set_canonical(self, canon):
        self.canonical = canon

    def set_code(self, code):
        self.code = int(code)

    def record(self):
        self.load_time = datetime.now() - self.time_init
        self.load_time = ((self.load_time.microseconds / 1000) +
                         (self.load_time.seconds * 1000)) # ms conversion
        self.url = self.http_host + self.path_info

        data = self.format_data()

        self.send_data(data)

        return data

    def get_url(self):
        return self.http_host + self.path_info

    def format_data(self, **kwargs):
        body = []

        params = dict({
            'id': settings.BOTIFY_CLIENT_ID,
            'api_key': settings.BOTIFY_API_KEY,
            'url': urllib.quote(self.get_url()),
            'time': int(time.time()),
            'code': self.code,
            'bot': '<ip>%s</ip><ua>%s</ua>' % (self.ip, self.user_agent),
            'load': self.load_time,
        }, **kwargs)

        for k, v in params.items():
            body.append(u'<%s>%s</%s>' % (k, v, k))

        if self.trackers:
            s = ""
            for tracker in self.trackers:
                s += "<t>%s</t>" % tracker
            body.append(u"<trackers>%s</trackers>" % s)

        if self.canonical :
            body.append(u"<canonical>%s</canonical>" %
                        urllib.quote(self.canonical))

        return u'<?xml version="2.0"?><crawl>%s</crawl>' % ''.join(body)

    @staticmethod
    def send_data(data):
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        udp_sock.sendto(data, settings.BOTIFY_SERVER)
