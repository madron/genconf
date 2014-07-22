from django.test import TestCase
from .. import utils

CLEANED_DATA = dict(
    project_name='customer_01',
    cpe1_router_type='c1841',
    cpe1_lan1_ip='',
    cpe1_lan1_standby_ip='',
    cpe1_line1_id='',
    cpe1_line1_access_type='adsl',
    cpe1_line1_cpeslotif='0/0',
    cpe1_line1_vc1_cpevcid='',
    cpe1_line1_vc1_loopback_ip='',
    cpe1_line1_vc2_cpevcid='',
    cpe1_line1_lan1_interface='',
    cpe1_line1_lan1_ip='',
    cpe1_line1_lan1_vrf='',
    cpe1_line1_lan2_interface='',
    cpe1_line1_lan2_ip='',
    cpe1_line1_lan2_vrf='',
    cpe2_router_type='c3550',
    cpe2_lan2_ip='',
    cpe2_lan2_standby_ip='',
    cpe2_line2_id='',
    cpe2_line2_access_type='shdsl',
    cpe2_line2_cpeslotif='0/1',
    cpe2_line2_vc1_cpevcid='',
    cpe2_line2_vc1_loopback_ip='',
    cpe2_line2_vc2_cpevcid='',
    cpe2_line2_lan1_interface='',
    cpe2_line2_lan1_ip='',
    cpe2_line2_lan1_vrf='',
    cpe2_line2_lan2_interface='',
    cpe2_line2_lan2_ip='',
    cpe2_line2_lan2_vrf='',
)


class UtilsTest(TestCase):
    def test_get_raw_config(self):
        config = utils.get_raw_config(CLEANED_DATA)
        # Common
        self.assertEqual(config['common']['project_name'], 'customer_01')
        self.assertEqual(len(config['common']['enable_secret']), 16)
        self.assertEqual(len(config['common']['vty_password']), 16)
        ### Cpe 1
        self.assertEqual(config['cpes'][0]['router_type'], 'c1841')
        # Lans
        lans = config['cpes'][0]['lans']
        self.assertEqual(len(lans), 1)
        self.assertEqual(lans[0]['ip'], '')
        self.assertEqual(lans[0]['standby_ip'], '')
        # Lines
        lines = config['cpes'][0]['lines']
        self.assertEqual(len(lines), 1)
        # Line 1
        self.assertEqual(lines[0]['access_type'], 'adsl')
        self.assertEqual(lines[0]['vcs'][0]['cpevcid'], '')
        self.assertEqual(lines[0]['vcs'][1]['cpevcid'], '')
        self.assertEqual(lines[0]['lans'][0]['interface'], '')
        self.assertEqual(lines[0]['lans'][1]['interface'], '')
        ### Cpe 2
        self.assertEqual(config['cpes'][1]['router_type'], 'c3550')
        # Lans
        lans = config['cpes'][1]['lans']
        self.assertEqual(len(lans), 2)
        self.assertEqual(lans[0], dict())
        self.assertEqual(lans[1]['ip'], '')
        self.assertEqual(lans[1]['standby_ip'], '')
        # Lines
        lines = config['cpes'][1]['lines']
        self.assertEqual(len(lines), 2)
        # Line 1
        self.assertEqual(lines[0], dict())
        # Line 2
        self.assertEqual(lines[1]['access_type'], 'shdsl')
        self.assertEqual(lines[1]['vcs'][0]['cpevcid'], '')
        self.assertEqual(lines[1]['vcs'][1]['cpevcid'], '')
        self.assertEqual(lines[1]['lans'][0]['interface'], '')
        self.assertEqual(lines[1]['lans'][1]['interface'], '')

    def test_get_raw_config_no_first_element(self):
        data = dict(
            project_name='customer_01',
            cpe2_line2_vc2_cpevcid='',
            cpe2_line2_lan2_ip='',
        )
        config = utils.get_raw_config(data)
        # Common
        self.assertEqual(config['common']['project_name'], 'customer_01')
        self.assertEqual(len(config['common']['enable_secret']), 16)
        self.assertEqual(len(config['common']['vty_password']), 16)
        # Cpe 1
        self.assertEqual(config['cpes'][0]['lines'], [])
        self.assertEqual(config['cpes'][0]['lans'], [])
        # Cpe 2
        self.assertEqual(config['cpes'][1]['lines'][1]['vcs'][0], dict())
        self.assertEqual(config['cpes'][1]['lines'][1]['vcs'][1]['cpevcid'], '')
        self.assertEqual(config['cpes'][1]['lines'][1]['lans'][0], dict())
        self.assertEqual(config['cpes'][1]['lines'][1]['lans'][1]['ip'], '')


    def test_get_custom_lan_config_c1841(self):
        config = dict()
        cpe = dict(router_type='c1841')
        lan = dict()
        lan_index = 1
        lan = utils.get_custom_lan_config(config, cpe, lan, lan_index)
        self.assertEqual(lan['custom_field'], 'Fx.20')


    def test_get_custom_vc_config_c3550(self):
        config = dict()
        cpe = dict(router_type='c3550')
        lan = dict()
        lan_index = 1
        lan = utils.get_custom_lan_config(config, cpe, lan, lan_index)
        self.assertEqual(lan['custom_field'], 'VLAN20')


    def test_get_cisco_config(self):
        cleaned_data = dict(
            project_name='project_name',
            cpe1_router_type='c1841',
            cpe1_lan1_standby_ip='cpe1_lan1_standby_ip',
            cpe1_lan2_standby_ip='cpe1_lan2_standby_ip',
            cpe1_lan3_standby_ip='cpe1_lan3_standby_ip',
            cpe1_line1_id='cpe1_line1_id',
            cpe1_line1_access_type='adsl',
            cpe1_line1_cpeslotif='0/0',
            cpe1_line1_vc1_brasname='cpe1_line1_vc1_brasname',
            cpe1_line1_vc1_brasvcid='cpe1_line1_vc1_brasvcid',
            cpe1_line1_vc1_brasip='cpe1_line1_vc1_brasip',
            cpe1_line1_vc1_cpevcid='cpe1_line1_vc1_cpevcid',
            cpe1_line1_vc1_cpeip='cpe1_line1_vc1_cpeip',
            cpe1_line1_vc1_cpedescr='cpe1_line1_vc1_cpedescr',
            cpe1_line1_vc1_loopback_ip='cpe1_line1_vc1_loopback_ip',
            cpe1_line1_vc2_brasname='cpe1_line1_vc2_brasname',
            cpe1_line1_vc2_brasvcid='cpe1_line1_vc2_brasvcid',
            cpe1_line1_vc2_brasip='cpe1_line1_vc2_brasip',
            cpe1_line1_vc2_cpevcid='cpe1_line1_vc2_cpevcid',
            cpe1_line1_vc2_cpeip='cpe1_line1_vc2_cpeip',
            cpe1_line1_vc2_cpedescr='cpe1_line1_vc2_cpedescr',
            cpe1_line1_vc3_brasname='cpe1_line1_vc3_brasname',
            cpe1_line1_vc3_brasvcid='cpe1_line1_vc3_brasvcid',
            cpe1_line1_vc3_brasip='cpe1_line1_vc3_brasip',
            cpe1_line1_vc3_cpevcid='cpe1_line1_vc3_cpevcid',
            cpe1_line1_vc3_cpeip='cpe1_line1_vc3_cpeip',
            cpe1_line1_vc3_cpedescr='cpe1_line1_vc3_cpedescr',
            cpe1_line1_lan1_interface='cpe1_line1_lan1_interface',
            cpe1_line1_lan1_ip='cpe1_line1_lan1_ip',
            cpe1_line1_lan1_vrf='cpe1_line1_lan1_vrf',
            cpe1_line1_lan2_interface='cpe1_line1_lan2_interface',
            cpe1_line1_lan2_ip='cpe1_line1_lan2_ip',
            cpe1_line1_lan2_vrf='cpe1_line1_lan2_vrf',
            cpe1_line1_lan3_interface='cpe1_line1_lan3_interface',
            cpe1_line1_lan3_ip='cpe1_line1_lan3_ip',
            cpe1_line1_lan3_vrf='cpe1_line1_lan3_vrf',
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
