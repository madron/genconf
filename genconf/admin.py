from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.core import urlresolvers
from adminwizard.admin import AdminWizard
from . import forms
from . import models
from . import views
from . import wizard_cpe2


class ReadOnlyTabularInline(admin.TabularInline):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def get_readonly_fields(self, request, obj=None):
        if self.fields:
            return self.fields
        fields = []
        for field in self.model._meta.get_all_field_names():
            if (not field == 'id'):
                fields.append(field)
        return fields


class ReadOnlyModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = list(set(
                [field.name for field in self.opts.local_fields if not field.name == 'id'] +
                [field.name for field in self.opts.local_many_to_many]
            ))
        return fields


class RouterConfigInline(admin.TabularInline):
    model = models.Router
    readonly_fields = ['name', 'model', 'configuration']
    fields = readonly_fields
    can_delete = False

    def has_add_permission(self, request):
        return False

    def configuration(self, obj):
        if not obj.pk:
            return ''
        info = (obj._meta.app_label, obj._meta.model_name)
        url_name = 'admin:%s_%s_configuration' % info
        config_url = urlresolvers.reverse(url_name, args=(obj.pk,))
        return '<a href="%s">%s</a>' % (config_url, obj)


class PhysicalLinkConfigInline(admin.TabularInline):
    model = models.PhysicalLink
    readonly_fields = ('router_interface_1', 'router_interface_2')
    fields = readonly_fields
    can_delete = False

    def has_add_permission(self, request):
        return False


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['wizard']
    fieldsets = [
        ['', dict(
            fields=[('name', 'wizard')],
        )],
        ['Wizard configuration', dict(
            classes=['collapse'],
            fields=['configuration'],
        )],
    ]
    inlines = [
        RouterConfigInline,
        PhysicalLinkConfigInline,
    ]

    def has_add_permission(self, request):
        return False


@admin.register(models.ProjectCpe2)
class ProjectCpe2Admin(AdminWizard):
    search_fields = ['name']
    exclude = ['wizard']
    save_on_top = True
    form = forms.ProjectForm
    wizard_view = wizard_cpe2.ProjectWizardView


class RouterInline(admin.TabularInline):
    model = models.Router
    readonly_fields = ['url', 'configuration']
    fields = ['url', 'name', 'model', 'configuration']
    # show_change_link will work with django 1.8
    show_change_link = True
    extra = 0

    def url(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_url(), obj)

    def configuration(self, obj):
        if not obj.pk:
            return ''
        info = (obj._meta.app_label, obj._meta.model_name)
        url_name = 'admin:%s_%s_configuration' % info
        config_url = urlresolvers.reverse(url_name, args=(obj.pk,))
        return '<a href="%s">%s</a>' % (config_url, obj)


class PhysicalLinkInline(admin.TabularInline):
    model = models.PhysicalLink
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PhysicalLinkInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name in ('router_interface_1', 'router_interface_2'):
            if request.obj:
                field.queryset = field.queryset.filter(router__project__pk=request.obj.pk)
            else:
                field.queryset = field.queryset.none()
        return field


@admin.register(models.ProjectCustom)
class ProjectCustomAdmin(admin.ModelAdmin):
    fields = ['name']
    inlines = [
        RouterInline,
        PhysicalLinkInline,
    ]

    def has_add_permission(self, request):
        return False

    def get_form(self, request, obj=None, **kwargs):
        request.obj = obj
        return super(ProjectCustomAdmin, self).get_form(request, obj, **kwargs)


class VrfInline(admin.TabularInline):
    model = models.Vrf
    extra = 0


class VlanInline(admin.TabularInline):
    model = models.Vlan
    form = forms.VlanForm
    extra = 0


class PhysicalInterfaceInline(admin.TabularInline):
    model = models.PhysicalInterface
    form = forms.PhysicalInterfaceForm
    readonly_fields = ['url']
    # show_change_link will work with django 1.8
    show_change_link = True
    extra = 0

    def url(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_url(), obj.name)

    def get_fields(self, request, obj=None):
        fields = super(PhysicalInterfaceInline, self).get_fields(request, obj=obj)
        # Move url at the beginning
        fields.remove('url')
        fields.insert(0, 'url')
        return fields


@admin.register(models.Router)
class RouterAdmin(admin.ModelAdmin):
    readonly_fields = ['project']
    change_form_template = 'genconf/router/change_form.html'
    fieldsets = [
        ['', dict(
            fields=[('project', 'name', 'model')],
        )],
    ]
    inlines = [
        VrfInline,
        VlanInline,
        PhysicalInterfaceInline,
    ]

    def get_queryset(self, request):
        qs = super(RouterAdmin, self).get_queryset(request)
        return qs.filter(project__wizard='')

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = patterns('',
            url(r'^(?P<pk>\d+)/configuration/$',
                self.admin_site.admin_view(views.ConfigurationView.as_view()),
                name='%s_%s_configuration' % info),
        )
        return urls + super(RouterAdmin, self).get_urls()

    def has_add_permission(self, request):
        return False


@admin.register(models.Vrf)
class VrfAdmin(ReadOnlyModelAdmin):
    pass


@admin.register(models.Route)
class RouteAdmin(ReadOnlyModelAdmin):
    pass


@admin.register(models.Vlan)
class VlanAdmin(ReadOnlyModelAdmin):
    pass


class SubInterfaceInline(admin.TabularInline):
    model = models.SubInterface
    form = forms.SubInterfaceForm
    fields = ('name', 'description', 'layer_3_interface', 'ipnetwork', 'vrf')
    extra = 0


@admin.register(models.PhysicalInterface)
class PhysicalInterfaceAdmin(admin.ModelAdmin):
    list_display = ['project', 'router', 'name', 'description', 'type', 'layer', 'mtu']
    list_display_links = ['name']
    form = forms.PhysicalInterfaceForm
    readonly_fields = ['router']
    fieldsets = (
        (None, dict(
            fields=(
                ('router', 'name', 'description'),
                ('type', 'layer', 'mtu'),
            ),
        )),
        ('Ethernet', dict(
            fields=(
                ('dot1q_mode', 'native_vlan', 'dot1q_encapsulation', 'duplex', 'speed'),
            ),
        )),
    )
    inlines = [
        SubInterfaceInline,
    ]

    def get_queryset(self, request):
        qs = super(PhysicalInterfaceAdmin, self).get_queryset(request)
        return qs.filter(router__project__wizard='')


@admin.register(models.SubInterface)
class SubInterfaceAdmin(ReadOnlyModelAdmin):
    pass


@admin.register(models.PhysicalLink)
class PhysicalLinkAdmin(ReadOnlyModelAdmin):
    pass


@admin.register(models.Layer3Interface)
class Layer3InterfaceAdmin(ReadOnlyModelAdmin):
    pass
