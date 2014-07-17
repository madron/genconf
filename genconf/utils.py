# import M2Crypto
import string
from django.template import Context, Template
from django.template.loader import get_template


def get_config(cleaned_data):
    config = dict(
        common=dict(),
        lines=[],
        lans=[],
    )
    for key, value in cleaned_data.iteritems():
        if key.startswith('line'):
            line_index = int(key[4:5]) - 1
            line_varname = key[6:]
            while line_index >= len(config['lines']):
                config['lines'].append(dict())
            if line_varname.startswith('vc'):
                vc_index = int(line_varname[2:3]) - 1
                vc_varname = line_varname[4:]
                if 'vcs' not in config['lines'][line_index]:
                    config['lines'][line_index]['vcs'] = []
                while vc_index >= len(config['lines'][line_index]['vcs']):
                    config['lines'][line_index]['vcs'].append(dict())
                config['lines'][line_index]['vcs'][vc_index][vc_varname] = value
            elif line_varname.startswith('lan'):
                lan_index = int(line_varname[3:4]) - 1
                lan_varname = line_varname[5:]
                if 'lans' not in config['lines'][line_index]:
                    config['lines'][line_index]['lans'] = []
                while lan_index >= len(config['lines'][line_index]['lans']):
                    config['lines'][line_index]['lans'].append(dict())
                config['lines'][line_index]['lans'][lan_index][lan_varname] = value
            else:
                config['lines'][line_index][line_varname] = value
        elif key.startswith('lan'):
            common_lan_index = int(key[3:4]) - 1
            common_lan_varname = key[5:]
            while common_lan_index >= len(config['lans']):
                config['lans'].append(dict())
            config['lans'][common_lan_index][common_lan_varname] = value
        else:
            config['common'][key] = value
    config['common']['enable_secret'] = random_password(length=16)
    config['common']['vty_password'] = random_password(length=16)
    return config


def random_password(length=16):
    return 'pippopippopippo1'
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    password = ''
    for i in range(length):
        password += chars[ord(M2Crypto.m2.rand_bytes(1)) % len(chars)]
    return password


def get_cisco_config(config, line):
    config['line'] = config['lines'][line]
    config['atm_access_types'] = ['adsl', 'shdsl']
    config['serial_access_types'] = ['hdsl']
    template = get_template('genconf/cisco.txt')
    context = Context(config)
    return template.render(context)
