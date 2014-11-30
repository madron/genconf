from django.core import urlresolvers
from django.db import models
from . import constants


class Project(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    configuration = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProjectWizard(Project):
    class Meta:
        proxy = True


class Router(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = (('project', 'name'),)
        index_together = (('project', 'name'),)

    def __str__(self):
        return self.name

    def get_url(self):
        app_label = self._meta.app_label
        model_name = self._meta.model_name
        url_name = 'admin:%s_%s_change' % (app_label, model_name)
        return urlresolvers.reverse(url_name, args=(self.pk,))


class Vrf(models.Model):
    router = models.ForeignKey(Router)
    name = models.CharField(max_length=50, blank=True)
    default_gateway = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = (('router', 'name'),)
        index_together = (('router', 'name'),)

    def __str__(self):
        return self.name or '<default>'

    @property
    def is_global(self):
        return not self.name


class Route(models.Model):
    vrf = models.ForeignKey(Vrf, db_index=True)
    name = models.CharField(max_length=50, blank=True)
    network = models.CharField(max_length=50, blank=True)
    next_hop = models.CharField(max_length=50, blank=True)
    metric = models.IntegerField(default=1)
    tag = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Layer3Interface(models.Model):
    vrf = models.ForeignKey(Vrf, db_index=True)
    description = models.CharField(max_length=200, blank=True)
    ipnetwork = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.description


class Vlan(models.Model):
    router = models.ForeignKey(Router)
    tag = models.IntegerField(default=1)
    layer_3_interface = models.OneToOneField(Layer3Interface, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = (('router', 'tag'),)
        index_together = (('router', 'tag'),)

    def __str__(self):
        if self.description:
            return '%d (%s)' % (self.tag, self.description)
        return str(self.tag)


class PhysicalInterface(models.Model):
    router = models.ForeignKey(Router)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=50, default='ethernet',
        choices=constants.INTERFACE_TYPE_CHOICES)
    layer = models.CharField(max_length=50, default='2',
        choices=((2, 2), (3, 3)),
        help_text="""Expresses how this interface is used
        (some interfaces can be configured as layer 2 or layer 3).
        layer 2 -> switching interface
        layer 3 -> routing interface
        """
    )
    mtu = models.IntegerField(default=1500)
    # Ethernet related fields
    duplex = models.CharField(max_length=50, default='auto')
    speed = models.CharField(max_length=50, default='auto')
    dot1q_mode = models.CharField(max_length=50, default='access',
        choices=constants.DOT1Q_MODE_CHOICES)
    dot1q_encapsulation = models.CharField(max_length=50, default='802.1q',
        choices=constants.DOT1Q_ENCAPSULATION_CHOICES)
    native_vlan = models.ForeignKey(Vlan)

    class Meta:
        unique_together = (('router', 'name'),)
        index_together = (('router', 'name'),)

    def __str__(self):
        return self.name

    @property
    def is_layer2(self):
        return self.layer == 2

    @property
    def is_layer3(self):
        return self.layer == 3


class SubInterface(models.Model):
    physical_interface = models.ForeignKey(PhysicalInterface)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default='ethernet',
        choices=constants.INTERFACE_TYPE_CHOICES)
    layer_3_interface = models.OneToOneField(Layer3Interface, blank=True, null=True,
        help_text="""Can be blank for type ethernet and layer 2.
        In all other cases is mandatory.
        """)
    description = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    # Ethernet related field
    layer = models.CharField(max_length=50, default='2',
        choices=((2, 2), (3, 3)),
        help_text="""Layer 3 -> subinterface with ip,
        layer 2 -> bridged to vlan.
        """)
    vlan = models.ForeignKey(Vlan)
    # Atm related fields
    link = models.CharField(max_length=50, default='point-to-point',
        choices=constants.ATM_LINK_CHOICES)
    pvc_vp = models.IntegerField(default=8)
    pvc_vc = models.IntegerField(default=35)
    pvc_encapsulation = models.CharField(max_length=50, default='pppoa',
        choices=constants.ATM_PVC_ENCAPSULATION_CHOICES)
    pvc_mux = models.CharField(max_length=50, default='vc-mux',
        choices=constants.ATM_PVC_MUX_CHOICES)
    pvc_dialer_pool_number = models.IntegerField(default=1)

    class Meta:
        unique_together = (('physical_interface', 'name'),)
        index_together = (('physical_interface', 'name'),)

    def __str__(self):
        return self.name
