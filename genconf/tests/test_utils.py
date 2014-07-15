from django.test import TestCase
from .. import utils

CLEANED_DATA = dict(
    project_name='customer_01',
    lan1_standby_ip='',
    lan2_standby_ip='',
    line1_id='',
    line1_access_type='adsl',
    line1_router_type='',
    line1_cpeslotif='',
    line1_vc1_cpevcid='',
    line1_vc1_loopback_ip='',
    line1_vc2_cpevcid='',
    line1_lan1_interface='',
    line1_lan1_ip='',
    line1_lan1_vrf='',
    line1_lan2_interface='',
    line1_lan2_ip='',
    line1_lan2_vrf='',
    line2_id='',
    line2_access_type='shdsl',
    line2_router_type='',
    line2_cpeslotif='',
    line2_vc1_cpevcid='',
    line2_vc1_loopback_ip='',
    line2_vc2_cpevcid='',
    line2_lan1_interface='',
    line2_lan1_ip='',
    line2_lan1_vrf='',
    line2_lan2_interface='',
    line2_lan2_ip='',
    line2_lan2_vrf='',
)


class UtilsTest(TestCase):
    def test_get_config(self):
        config = utils.get_config(CLEANED_DATA)
        # from pprint import pprint
        # pprint(config)
        # Common
        self.assertEqual(config['common']['project_name'], 'customer_01')
        self.assertEqual(len(config['common']['enable_secret']), 16)
        self.assertEqual(len(config['common']['vty_password']), 16)
        # Lans
        self.assertEqual(config['lans'][0]['standby_ip'], '')
        self.assertEqual(config['lans'][1]['standby_ip'], '')
        # Line 1
        self.assertEqual(config['lines'][0]['access_type'], 'adsl')
        self.assertEqual(config['lines'][0]['vcs'][0]['cpevcid'], '')
        self.assertEqual(config['lines'][0]['vcs'][1]['cpevcid'], '')
        self.assertEqual(config['lines'][0]['lans'][0]['interface'], '')
        self.assertEqual(config['lines'][0]['lans'][1]['interface'], '')
        # Line 2
        self.assertEqual(config['lines'][1]['access_type'], 'shdsl')
        self.assertEqual(config['lines'][1]['vcs'][0]['cpevcid'], '')
        self.assertEqual(config['lines'][1]['vcs'][1]['cpevcid'], '')
        self.assertEqual(config['lines'][1]['lans'][0]['interface'], '')
        self.assertEqual(config['lines'][1]['lans'][1]['interface'], '')

    def test_get_cisco_config(self):
        config = utils.get_cisco_config(utils.get_config(CLEANED_DATA), 0)
        start = 0
        lines = config.splitlines()
        for i in range(start, start + 35):
            print lines[i]
        self.assertTrue('boot-start-marker' in config)
