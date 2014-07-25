ROUTER_TYPE_CHOICES = (
    ('c1841', 'Cisco 1841'),
    ('c1801', 'Cisco 1801'),
    ('c3550', 'Cisco 3550'),
)

ACCESS_TYPE_CHOICES = (
    ('adsl', 'Adsl'),
    ('eth', 'Ethernet'),
    ('hdsl-fr', 'Hdsl frame relay'),
    ('shdsl', 'Shdsl ATM'),
)

VC_TYPE_CHOICES = (
    ('ipaccess', 'IP Access'),
    ('voip', 'Voip Mynet'),
    ('vpn', 'Vpn Mpls'),
)

BRAS_TYPE_CHOICES = (
    ('mantitau-10k', 'Cisco 10K Mantova'),
    ('bresitaw-10k', 'Cisco 10K Brescia'),
    ('milaitcc-10k', 'Cisco 10K Milano Bersaglio'),
    ('micalenter-10k', 'Cisco 10K MilCal Enter'),
)

BRASLOOP_TYPE_CHOICES = (
    ('loop2', 'Loopback2'),
    ('loop3', 'Loopback3'),
    ('loop4', 'Loopback4'),
    ('loop5', 'Loopback5'),
    ('loop6', 'Loopback6'),
    ('loop7', 'Loopback7'),
)

BRAS_DEFAULT_LOOPBACK = 'loop2'

BRAS_LOOPBACK_IP = dict(
    mantitau10k=dict(
        loop2='93.91.128.254',
        loop3='93.91.128.245',
        loop4='93.91.128.244',
        loop5='93.91.128.243',
        loop6='93.91.128.242',
        loop7='93.91.128.233',
    ),
    bresitaw10k=dict(
        loop2='93.91.128.227',
        loop3='93.91.128.228',
    ),
    milaitcc10k=dict(
        loop2='93.91.128.224',
        loop3='93.91.128.225',
        loop4='93.91.128.223',
        loop5='93.91.128.222',
        loop6='93.91.128.221',
    ),
    micalenter10k=dict(
        loop2='93.91.128.251',
        loop3='93.91.128.250',
        loop4='93.91.128.241',
        loop5='93.91.128.240',
        loop6='93.91.128.239',
        loop7='93.91.128.229',
    ),
)