from .settings_common import *

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    # '--with-coverage',
    # '--cover-html',
    '--cover-branches',
    '--cover-erase',
    '--cover-package=genconf,dictserializer',
    '--cover-inclusive',
    '--cover-html-dir=coverage',
]
