from django.core import urlresolvers
from django.db import models
from django.utils.translation import ugettext_lazy as _
from netaddr import IPNetwork
from netutils.modelfields import NetIPNetworkField
from . import constants
from . import hardware


class Project(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    wizard = models.CharField(max_length=50, db_index=True,
        choices=constants.PROJECT_WIZARD_CHOICES, blank=True)
    configuration = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProjectCustomManager(models.Manager):
    def get_queryset(self):
        qs = super(ProjectCustomManager, self).get_queryset()
        return qs.filter(wizard='')


class ProjectCustom(Project):
    objects = ProjectCustomManager()

    class Meta:
        proxy = True
        verbose_name = 'project custom'
        verbose_name_plural = 'projects custom'


class ProjectCpe2Manager(models.Manager):
    def get_queryset(self):
        qs = super(ProjectCpe2Manager, self).get_queryset()
        return qs.filter(wizard='cpe2')


class ProjectCpe2(Project):
    objects = ProjectCpe2Manager()

    class Meta:
        proxy = True
        verbose_name = 'project cpe 2'
        verbose_name_plural = 'projects cpe 2'

    def save(self, *args, **kwargs):
        self.wizard = 'cpe2'
        return super(ProjectCpe2, self).save(*args, **kwargs)


class Router(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=50,
        choices=constants.ROUTER_TYPE_CHOICES)

    class Meta:
        unique_together = (('project', 'name'),)
        index_together = (('project', 'name'),)

    def __str__(self):
        return self.name

    def get_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        url_name = 'admin:%s_%s_change' % info
        return urlresolvers.reverse(url_name, args=(self.pk,))

    @property
    def link(self):
        return '<a href="%s">%s</a>' % (self.get_url(), self)

    def get_interface_names(self, type=None, layer=None):
        interfaces = hardware.ROUTER_TYPE.get(self.model, dict(interfaces=[]))['interfaces']
        if type:
            interfaces = [i for i in interfaces if i['type'] == type]
        if layer:
            interfaces = [i for i in interfaces if i['layer'] == layer]
        return [i['name'] for i in interfaces]


class Vrf(models.Model):
    router = models.ForeignKey(Router)
    name = models.CharField(max_length=50, blank=True)
    default_gateway = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = (('router', 'name'),)
        index_together = (('router', 'name'),)

    def __str__(self):
        return self.name or '(default)'

    @property
    def is_global(self):
        return not self.name

    def delete_vrf_link(self):
        if self.pk:
            label = str(self)
            if not self.name:
                return label
            info = (self._meta.app_label, self._meta.model_name)
            url_name = 'admin:%s_%s_delete' % info
            delete_url = urlresolvers.reverse(url_name, args=(self.pk,))
            return '<a href="%s">%s</a>' % (delete_url, label)
        return ''
    delete_vrf_link.short_description = _('delete')


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
    ipnetwork = NetIPNetworkField(null=True, blank=True)

    class Meta:
        verbose_name = 'layer 3 interface'

    def __str__(self):
        return str(self.ipnetwork)

    def get_ipnetwork(self):
        return IPNetwork(self.ipnetwork)


class Vlan(models.Model):
    router = models.ForeignKey(Router)
    tag = models.IntegerField()
    description = models.CharField(max_length=200, blank=True)
    layer_3_interface = models.OneToOneField(Layer3Interface, blank=True, null=True)

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
    type = models.CharField(max_length=50, default='atm',
        choices=constants.INTERFACE_TYPE_CHOICES)
    layer = models.CharField(max_length=50, default='2',
        choices=(('2', '2'), ('3', '3')),
        help_text="""Expresses how this interface is used
        (some interfaces can be configured as layer 2 or layer 3).
        Layer 2 -> switching interface.
        Layer 3 -> routing interface.
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
    native_vlan = models.ForeignKey(Vlan, blank=True, null=True)

    class Meta:
        unique_together = (('router', 'name'),)
        index_together = (('router', 'name'),)

    def __str__(self):
        return ('%s %s' % (self.router, self.name)).strip()

    @property
    def project(self):
        return self.router.project

    @property
    def is_layer2(self):
        return self.layer == 2

    @property
    def is_layer3(self):
        return self.layer == 3

    def get_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        url_name = 'admin:%s_%s_change' % info
        return urlresolvers.reverse(url_name, args=(self.pk,))


class SubInterface(models.Model):
    physical_interface = models.ForeignKey(PhysicalInterface)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    layer_3_interface = models.OneToOneField(Layer3Interface, blank=True, null=True,
        help_text="""Can be blank for type ethernet and layer 2.
        In all other cases is mandatory.""")
    # Ethernet related field
    layer = models.CharField(max_length=50, default='2',
        choices=(('2', '2'), ('3', '3')),
        help_text="""Layer 3 -> subinterface with ip,
        layer 2 -> bridged to vlan.
        """)
    vlan = models.ForeignKey(Vlan, blank=True, null=True)
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

    def get_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        url_name = 'admin:%s_%s_change' % info
        return urlresolvers.reverse(url_name, args=(self.pk,))


class PhysicalLink(models.Model):
    project = models.ForeignKey(Project, db_index=True)
    router_interface_1 = models.ForeignKey(PhysicalInterface,
        related_name='%(app_label)s_%(class)s_router_interface_1_pk')
    router_interface_2 = models.ForeignKey(PhysicalInterface,
        related_name='%(app_label)s_%(class)s_router_interface_2_pk')

    def __str__(self):
        return '%s <-> %s' % (self.router_interface_1, self.router_interface_2)
