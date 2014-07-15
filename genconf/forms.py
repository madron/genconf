from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit
from crispy_forms.layout import Row, HTML
from django import forms
from django.utils.translation import ugettext as _

ACCESS_TYPE_CHOICES = (
    ('adsl', 'Adsl'),
    ('eth', 'Ethernet'),
    ('hdsl_fr', 'Hdsl frame relay'),
    ('shdsl', 'Shdsl ATM'),
)
ROUTER_TYPE_CHOICES = (
    ('c1841', 'Cisco 1841'),
    ('c1801', 'Cisco 1801'),
    ('c3550', 'Cisco 3550'),
)


class LineForm(forms.Form):
    id = forms.CharField(required=False)
    access_type = forms.ChoiceField(choices=ACCESS_TYPE_CHOICES)
    router_type = forms.ChoiceField(choices=ROUTER_TYPE_CHOICES)
    cpeslotif = forms.CharField(required=False)


class VcForm(forms.Form):
    brasname = forms.CharField(required=False)
    brasvcid = forms.CharField(required=False)
    brasip = forms.CharField(required=False)
    cpevcid = forms.CharField(required=False)
    cpeip = forms.CharField(required=False)
    loopback_ip = forms.CharField(required=False)


class GenConfForm(forms.Form):
    project_name = forms.CharField(required=True)

    lan1_standby_ip = forms.CharField(required=False)
    lan2_standby_ip = forms.CharField(required=False)
    lan3_standby_ip = forms.CharField(required=False)

    line1_id = forms.CharField(required=False)
    line1_access_type = forms.ChoiceField(choices=ACCESS_TYPE_CHOICES)
    line1_router_type = forms.ChoiceField(choices=ROUTER_TYPE_CHOICES)
    line1_cpeslotif = forms.CharField(required=False)

    line1_vc1_brasname = forms.CharField(required=False)
    line1_vc1_brasvcid = forms.CharField(required=False)
    line1_vc1_brasip = forms.CharField(required=False)
    line1_vc1_cpevcid = forms.CharField(required=False)
    line1_vc1_cpeip = forms.CharField(required=False)
    line1_vc1_loopback_ip = forms.CharField(required=False)

    line1_vc2_brasname = forms.CharField(required=False)
    line1_vc2_brasvcid = forms.CharField(required=False)
    line1_vc2_brasip = forms.CharField(required=False)
    line1_vc2_cpevcid = forms.CharField(required=False)
    line1_vc2_cpeip = forms.CharField(required=False)
    line1_vc3_brasname = forms.CharField(required=False)
    line1_vc3_brasvcid = forms.CharField(required=False)
    line1_vc3_brasip = forms.CharField(required=False)
    line1_vc3_cpevcid = forms.CharField(required=False)
    line1_vc3_cpeip = forms.CharField(required=False)

    line1_lan1_interface = forms.CharField(required=False)
    line1_lan1_ip = forms.CharField(required=False)
    line1_lan1_vrf = forms.CharField(required=False)
    line1_lan2_interface = forms.CharField(required=False)
    line1_lan2_ip = forms.CharField(required=False)
    line1_lan2_vrf = forms.CharField(required=False)
    line1_lan3_interface = forms.CharField(required=False)
    line1_lan3_ip = forms.CharField(required=False)
    line1_lan3_vrf = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        # self.helper.form_method = 'get'
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'Submit'))
        # self.helper.layout = self.get_layout()
        super(GenConfForm, self).__init__(*args, **kwargs)

    def get_layout(self):
        layout = Layout(
            layout.Div('pppppp'),
            layout.HTML('<div class="jumbotron"> <h1>Hello, world!</h1> <p>...</p> <p><a class="btn btn-primary btn-lg" role="button">Learn more</a></p> </div>'),
            layout.Div(Field('line1_lan1_interface', css_class="hero")),
            Fieldset(
                _('Common'),
                'project_name',
            ),
            ButtonHolder(
                Submit('submit', _('Submit'), css_class='btn btn-primary')
            )
        )
        return layout