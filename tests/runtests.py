#!/usr/bin/env python
import os
import sys
import coverage

from django.conf import settings

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        INSTALLED_APPS=[
            'botify',
            'tests',
        ],

        ROOT_URLCONF='urls',

        MIDDLEWARE_CLASSES = (
            'botify.middleware.BotifyMiddleware',
        ),

        TEST_DIR=TEST_DIR,

        BOTIFY_CLIENT_ID = 0,
        BOTIFY_SERVER = ('fake.server.botify.sem.io', 8181),
        BOTIFY_API_KEY = '9e3b55ec53567922f8b75f5e3c8a543ff9e7fe2ea8'
    )

from django.test.simple import run_tests


def runtests(*test_args):
    if not test_args:
        test_args = ['tests']

    parent_dir = os.path.join(TEST_DIR, "../")

    sys.path.insert(0, parent_dir)
    cover = coverage.coverage(branch=True, cover_pylib=False,
        include=[
            os.path.join(parent_dir, 'botify', '*.py'),
        ],
        omit=[
        ]
    )
    cover.load()
    cover.start()
    failures = run_tests(test_args, verbosity=1, interactive=True)
    cover.stop()
    cover.save()
    cover.report(file=sys.stdout)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
