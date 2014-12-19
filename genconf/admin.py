from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from adminwizard.admin import AdminWizard
from . import forms
from . import models
from . import views


class ReadOnlyTabularInline(admin.TabularInline):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, object):
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


@admin.register(models.ProjectWizard)
class ProjectAdminWizard(AdminWizard):
    form = forms.ProjectForm
    search_fields = ['name']
    save_on_top = True
    save_as = True
    wizard_view = views.ProjectWizardView


@admin.register(models.ProjectCpe2)
class ProjectCpe2Admin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['wizard']
    save_on_top = True


class RouterInline(ReadOnlyTabularInline):
    model = models.Router
    fields = ('url',)
    # show_change_link will work with django 1.8
    show_change_link = True

    def url(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_url(), obj)


class PhysicalLinkInline(ReadOnlyTabularInline):
    model = models.PhysicalLink
    fields = ('router_interface_1', 'router_interface_2')


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('type',)
    inlines = [
        RouterInline,
        PhysicalLinkInline,
    ]

    def has_add_permission(self, request):
        return False


class VlanInline(ReadOnlyTabularInline):
    model = models.Vlan
    fields = ('__str__', 'layer3interface', 'notes')


@admin.register(models.Router)
class RouterAdmin(ReadOnlyModelAdmin):
    change_form_template = 'genconf/router/change_form.html'
    inlines = [
        VlanInline,
    ]

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = patterns('',
            url(r'^(?P<pk>\d+)/configuration/$',
                self.admin_site.admin_view(views.ConfigurationView.as_view()),
                name='%s_%s_configuration' % info),
        )
        return urls + super(RouterAdmin, self).get_urls()


@admin.register(models.Vrf)
class VrfAdmin(ReadOnlyModelAdmin):
    pass


@admin.register(models.Route)
class RouteAdmin(ReadOnlyModelAdmin):
    pass


@admin.register(models.Vlan)
class VlanAdmin(ReadOnlyModelAdmin):
    pass


class SubInterfaceInline(ReadOnlyTabularInline):
    model = models.SubInterface
    fields = ('name', 'type', 'layer3interface', 'description', 'notes')


@admin.register(models.PhysicalInterface)
class PhysicalInterfaceAdmin(ReadOnlyModelAdmin):
    inlines = [
        SubInterfaceInline,
    ]


@admin.register(models.SubInterface)
class SubInterfaceAdmin(ReadOnlyModelAdmin):
    pass


@admin.register(models.PhysicalLink)
class PhysicalLinkAdmin(ReadOnlyModelAdmin):
    pass


@admin.register(models.Layer3Interface)
class Layer3InterfaceAdmin(ReadOnlyModelAdmin):
    pass
