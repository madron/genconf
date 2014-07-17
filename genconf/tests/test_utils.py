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

    def test_get_config_no_line1(self):
        data = dict(
            project_name='customer_01',
            line2_vc2_cpevcid='',
            line2_lan2_ip='',
        )
        config = utils.get_config(data)
        # Common
        self.assertEqual(config['common']['project_name'], 'customer_01')
        self.assertEqual(len(config['common']['enable_secret']), 16)
        self.assertEqual(len(config['common']['vty_password']), 16)
        # Line 1
        self.assertEqual(config['lines'][0], dict())
        # Line 2
        self.assertEqual(config['lines'][1]['vcs'][0], dict())
        self.assertEqual(config['lines'][1]['vcs'][1]['cpevcid'], '')
        self.assertEqual(config['lines'][1]['lans'][0], dict())
        self.assertEqual(config['lines'][1]['lans'][1]['ip'], '')

    def test_get_cisco_config(self):
        cleaned_data = dict(
            project_name='project_name',
            lan1_standby_ip='lan1_standby_ip',
            lan2_standby_ip='lan2_standby_ip',
            lan3_standby_ip='lan3_standby_ip',
            line1_id='line1_id',
            line1_access_type='adsl',
            line1_router_type='line1_router_type',
            line1_cpeslotif='0/0',
            line1_vc1_brasname='line1_vc1_brasname',
            line1_vc1_brasvcid='line1_vc1_brasvcid',
            line1_vc1_brasip='line1_vc1_brasip',
            line1_vc1_cpevcid='line1_vc1_cpevcid',
            line1_vc1_cpeip='line1_vc1_cpeip',
            line1_vc1_cpedescr='line1_vc1_cpedescr',
            line1_vc1_loopback_ip='line1_vc1_loopback_ip',
            line1_vc2_brasname='line1_vc2_brasname',
            line1_vc2_brasvcid='line1_vc2_brasvcid',
            line1_vc2_brasip='line1_vc2_brasip',
            line1_vc2_cpevcid='line1_vc2_cpevcid',
            line1_vc2_cpeip='line1_vc2_cpeip',
            line1_vc2_cpedescr='line1_vc2_cpedescr',
            line1_vc3_brasname='line1_vc3_brasname',
            line1_vc3_brasvcid='line1_vc3_brasvcid',
            line1_vc3_brasip='line1_vc3_brasip',
            line1_vc3_cpevcid='line1_vc3_cpevcid',
            line1_vc3_cpeip='line1_vc3_cpeip',
            line1_vc3_cpedescr='line1_vc3_cpedescr',
            line1_lan1_interface='line1_lan1_interface',
            line1_lan1_ip='line1_lan1_ip',
            line1_lan1_vrf='line1_lan1_vrf',
            line1_lan2_interface='line1_lan2_interface',
            line1_lan2_ip='line1_lan2_ip',
            line1_lan2_vrf='line1_lan2_vrf',
            line1_lan3_interface='line1_lan3_interface',
            line1_lan3_ip='line1_lan3_ip',
            line1_lan3_vrf='line1_lan3_vrf',
        )
        config = utils.get_config(cleaned_data)
        from pprint import pprint
        pprint(config)
        cisco = utils.get_cisco_config(config, 0)
        start = 40
        lines = cisco.splitlines()
        for i in range(start, start + 35):
            print lines[i]
        self.assertTrue('boot-start-marker' in cisco)
