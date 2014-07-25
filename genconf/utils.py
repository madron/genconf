# import M2Crypto
import string
from netaddr import *
from django.template import Context, Template
from django.template.loader import get_template
from . import constants


def get_config(cleaned_data):
    config = get_raw_config(cleaned_data)
    return get_custom_config(config)


def get_raw_config(cleaned_data):
    config = dict(
        common=dict(),
        cpes=[],
    )
    for key, value in cleaned_data.iteritems():
        if key.startswith('cpe'):
            cpe_index = int(key[3:4]) - 1
            cpe_varname = key[5:]
            while cpe_index >= len(config['cpes']):
                config['cpes'].append(dict(lines=[], lans=[]))
            if cpe_varname.startswith('line'):
                line_index = int(cpe_varname[4:5]) - 1
                line_varname = cpe_varname[6:]
                while line_index >= len(config['cpes'][cpe_index]['lines']):
                    config['cpes'][cpe_index]['lines'].append(dict())
                if line_varname.startswith('vc'):
                    vc_index = int(line_varname[2:3]) - 1
                    vc_varname = line_varname[4:]
                    if 'vcs' not in config['cpes'][cpe_index]['lines'][line_index]:
                        config['cpes'][cpe_index]['lines'][line_index]['vcs'] = []
                    while vc_index >= len(config['cpes'][cpe_index]['lines'][line_index]['vcs']):
                        config['cpes'][cpe_index]['lines'][line_index]['vcs'].append(dict())
                    config['cpes'][cpe_index]['lines'][line_index]['vcs'][vc_index][vc_varname] = value
                elif line_varname.startswith('lan'):
                    lan_index = int(line_varname[3:4]) - 1
                    lan_varname = line_varname[5:]
                    if 'lans' not in config['cpes'][cpe_index]['lines'][line_index]:
                        config['cpes'][cpe_index]['lines'][line_index]['lans'] = []
                    while lan_index >= len(config['cpes'][cpe_index]['lines'][line_index]['lans']):
                        config['cpes'][cpe_index]['lines'][line_index]['lans'].append(dict())
                    config['cpes'][cpe_index]['lines'][line_index]['lans'][lan_index][lan_varname] = value
                else:
                    config['cpes'][cpe_index]['lines'][line_index][line_varname] = value
            elif cpe_varname.startswith('lan'):
                common_lan_index = int(cpe_varname[3:4]) - 1
                common_lan_varname = cpe_varname[5:]
                while common_lan_index >= len(config['cpes'][cpe_index]['lans']):
                    config['cpes'][cpe_index]['lans'].append(dict())
                config['cpes'][cpe_index]['lans'][common_lan_index][common_lan_varname] = value
            else:
                config['cpes'][cpe_index][cpe_varname] = value
        else:
            config['common'][key] = value
    config['common']['enable_secret'] = random_password(length=16)
    config['common']['vty_password'] = random_password(length=16)
    return config


def get_custom_config(config):
    for cpe in config['cpes']:
        cpe = get_custom_cpe_config(config, cpe)
    return config


def get_custom_cpe_config(config, cpe):
    for line_index, line in enumerate(cpe['lines']):
        line = get_custom_line_config(config, cpe, line, line_index)
    for lan_index, lan in enumerate(cpe['lans']):
        lan = get_custom_lan_config(config, cpe, lan, lan_index)
    return config


def get_custom_line_config(config, cpe, line, line_index):
    for vc_index, vc in enumerate(line['vcs']):
        vc = get_custom_vc_config(config, cpe, line, vc, vc_index)


def get_custom_vc_config(config, cpe, line, vc, vc_index):
    vc['idx'] = vc_index
    vc['ppppwd'] = random_password(length=16)
    vc.update(get_vc_subnet_parameters(vc))
    return vc


def get_vc_subnet_parameters(vc):
    subnet = IPNetwork(vc['cpeip'])
    subnet_mask = subnet.netmask.format()
    subnet_mask_bits = subnet.prefixlen
    if (subnet_mask_bits == 32):
        bras_id = vc['brasname']
        loopback = vc.get('loopback', constants.BRAS_DEFAULT_LOOPBACK)
        ip = (subnet.network).format()
        bras_ip = constants.BRAS_LOOPBACK_IP[bras_id][loopback]
    else:
        ip = (subnet.network + 2).format()
        bras_ip = (subnet.network + 1).format()
    return dict(
        brasip=bras_ip,
        cpeipadd=ip,
        cpeipmask=subnet_mask,
        cpeipprefixlen=subnet_mask_bits,
    )


def get_custom_lan_config(config, cpe, lan, lan_index):
    lans = len(cpe['lans'])
    lan['stbyindex'] = ((lan_index + 1) * 10 )
    if (cpe['router_type'] == 'c1841' and lans < 3):
        lan['ifidx'] = 'FastEthernet%d/0' % (lan_index)
    elif (cpe['router_type'] == 'c1841' and lans > 2 and lan_index == 1):
        lan['ifidx'] = 'FastEthernet%d/0' % (lan_index)
    elif (cpe['router_type'] == 'c1841' and lans > 2):
        lan['ifidx'] = 'FastEthernet0/0.%d' % (lan_index + 1)
    elif cpe['router_type'] == 'c3550':
        lan['ifidx'] = 'VLAN%d0' % (lan_index + 1)
    ip = IPNetwork(lan['ip'])
    lan['ipadd'] = ip.ip.format()
    lan['ipmask'] = ip.netmask.format()
    lan['nat'] = IPAddress(ip).is_private() and not lan['vrf']
    return lan


def random_password(length=16):
    return 'pippopippopippo1'
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    password = ''
    for i in range(length):
        password += chars[ord(M2Crypto.m2.rand_bytes(1)) % len(chars)]
    return password


def get_cisco_config(config, cpe):
    config['cpe'] = config['cpes'][cpe]
    config['atm_access_types'] = ['adsl', 'shdsl']
    config['serial_access_types'] = ['hdsl']
    template = get_template('genconf/cisco.txt')
    context = Context(config)
    return template.render(context)
