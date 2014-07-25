from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit
from crispy_forms.layout import Row, HTML
from django import forms
from django.utils.translation import ugettext as _
from . import constants


class LineForm(forms.Form):
    id = forms.CharField(required=False)
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)
    router_type = forms.ChoiceField(choices=constants.ROUTER_TYPE_CHOICES)
    cpeslotif = forms.CharField(required=False)


class VcForm(forms.Form):
    bras_id = forms.ChoiceField(choices=constants.BRAS_TYPE_CHOICES)
    brasvcid = forms.CharField(required=False)
    bras_ip = forms.CharField(required=False)
    cpevcid = forms.CharField(required=False)
    subnet = forms.CharField(required=False)
    loopback = forms.ChoiceField(choices=constants.BRASLOOP_TYPE_CHOICES)
    type = forms.ChoiceField(choices=constants.VC_TYPE_CHOICES)


class GenConfForm(forms.Form):
    project_name = forms.CharField(required=True)
    bgpas = forms.CharField(required=False)

    cpe1_router_type = forms.ChoiceField(choices=constants.ROUTER_TYPE_CHOICES)

    cpe1_lan1_ip = forms.CharField(required=False)
    cpe1_lan1_standby_ip = forms.CharField(required=False)
    cpe1_lan2_ip = forms.CharField(required=False)
    cpe1_lan2_standby_ip = forms.CharField(required=False)
    cpe1_lan3_ip = forms.CharField(required=False)
    cpe1_lan3_standby_ip = forms.CharField(required=False)

    cpe1_line1_id = forms.CharField(required=False)
    cpe1_line1_access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)
    cpe1_line1_cpeslotif = forms.CharField(required=False)

    cpe1_line1_vc1_bras_id = forms.CharField(required=False)
    cpe1_line1_vc1_brasvcid = forms.CharField(required=False)
    cpe1_line1_vc1_bras_ip = forms.CharField(required=False)
    cpe1_line1_vc1_cpevcid = forms.CharField(required=False)
    cpe1_line1_vc1_subnet = forms.CharField(required=False)
    cpe1_line1_vc1_cpedescr = forms.CharField(required=False)
    cpe1_line1_vc1_loopback = forms.CharField(required=False)
    cpe1_line1_vc1_bgp = forms.BooleanField()

    cpe1_line1_vc2_bras_id = forms.CharField(required=False)
    cpe1_line1_vc2_brasvcid = forms.CharField(required=False)
    cpe1_line1_vc2_bras_ip = forms.CharField(required=False)
    cpe1_line1_vc2_cpevcid = forms.CharField(required=False)
    cpe1_line1_vc2_subnet = forms.CharField(required=False)
    cpe1_line1_vc2_cpedescr = forms.CharField(required=False)
    cpe1_line1_vc2_loopback = forms.CharField(required=False)
    cpe1_line1_vc2_bgp = forms.BooleanField()

    cpe1_line1_vc3_bras_id = forms.CharField(required=False)
    cpe1_line1_vc3_brasvcid = forms.CharField(required=False)
    cpe1_line1_vc3_bras_ip = forms.CharField(required=False)
    cpe1_line1_vc3_cpevcid = forms.CharField(required=False)
    cpe1_line1_vc3_subnet = forms.CharField(required=False)
    cpe1_line1_vc3_cpedescr = forms.CharField(required=False)
    cpe1_line1_vc3_loopback = forms.CharField(required=False)
    cpe1_line1_vc3_bgp = forms.BooleanField()

    cpe1_lan1_descr = forms.CharField(required=False)
    cpe1_lan1_ip = forms.CharField(required=False)
    cpe1_lan1_vrf = forms.CharField(required=False)
    cpe1_lan2_descr = forms.CharField(required=False)
    cpe1_lan2_ip = forms.CharField(required=False)
    cpe1_lan2_vrf = forms.CharField(required=False)
    cpe1_lan3_descr = forms.CharField(required=False)
    cpe1_lan3_ip = forms.CharField(required=False)
    cpe1_lan3_vrf = forms.CharField(required=False)

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