from setuptools import setup, find_packages

VERSION = 0.1

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'botify seo sem django'

setup(
    name='botify',
    version=VERSION,
    description='Django app for botify',
    author='Amaury de la Vieuville',
    author_email='amaury.dlv@gmail.com',
    url='http://github.com/semio/django-botify',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
)
