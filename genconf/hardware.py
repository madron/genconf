from collections import OrderedDict


ROUTER_TYPE = OrderedDict([
    (
        'c1801',
        dict(
            brand='Cisco',
            model='1801',
            interfaces=[
                dict(name='atm0', type='atm', layer=3),
                dict(name='fe0', type='ethernet', layer=3),
                dict(name='fe1', type='ethernet', layer=2),
                dict(name='fe2', type='ethernet', layer=2),
                dict(name='fe3', type='ethernet', layer=2),
                dict(name='fe4', type='ethernet', layer=2),
                dict(name='fe5', type='ethernet', layer=2),
                dict(name='fe6', type='ethernet', layer=2),
                dict(name='fe7', type='ethernet', layer=2),
                dict(name='fe8', type='ethernet', layer=2),
            ],
            slots=[],
        )
    ),
    (
        'c1841',
        dict(
            brand='Cisco',
            model='1841',
            interfaces=[
                dict(name='fe0/0', type='ethernet', layer=3),
                dict(name='fe0/1', type='ethernet', layer=3),
            ],
            slots=[
                dict(number='0', type='wic'),
                dict(number='1', type='wic'),
            ],
        )
    ),
])

MODULE_TYPE = dict(
    hwic1adsl=dict(
        brand='Cisco',
        model='HWIC-1ADSL',
        type='wic',
        interfaces=[
            dict(name='atm', number='0', type='atm', layer=3),
        ],
    ),
    hwic2fe=dict(
        brand='Cisco',
        model='HWIC-2FE',
        type='wic',
        interfaces=[
            dict(name='fe', number='0', type='ethernet', layer=3),
            dict(name='fe', number='1', type='ethernet', layer=3),
        ],
    ),
)
