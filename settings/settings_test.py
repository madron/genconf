from .settings_common import *

INSTALLED_APPS = list(INSTALLED_APPS)
# INSTALLED_APPS.append('django_nose')

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    # '--with-coverage',
    # '--cover-html',
    '--nocapture',
    '--cover-branches',
    '--cover-erase',
    '--cover-package=genconf,dictserializer,netutils',
    '--cover-inclusive',
    '--cover-html-dir=coverage',
]
