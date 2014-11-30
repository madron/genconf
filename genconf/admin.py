from django.conf.urls import patterns, url
from django.contrib import admin
from django.utils.translation import ugettext as _
from adminwizard.admin import AdminWizard
from . import forms
from . import models
from . import views


@admin.register(models.ProjectWizard)
class ProjectAdminWizard(AdminWizard):
    form = forms.ProjectForm
    search_fields = ['name']
    save_on_top = True
    save_as = True
    wizard_view = views.ProjectWizardView


class RouterInline(admin.TabularInline):
    model = models.Router
    fields = ('name', 'change')
    readonly_fields = ('change',)
    # show_change_link will work with django 1.8
    show_change_link = True

    def change(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_url(), obj)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        RouterInline,
    ]


class VlanInline(admin.TabularInline):
    model = models.Vlan
    readonly_fields = ('notes',)


@admin.register(models.Router)
class RouterAdmin(admin.ModelAdmin):
    readonly_fields = ('project',)
    change_form_template = 'genconf/router/change_form.html'
    inlines = [
        VlanInline,
    ]

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = patterns('',
            url(r'^(?P<pk>\d+)/configuration/$',
                self.admin_site.admin_view(views.ConfigurationView.as_view()),
                name='%s_%s_configuration' % info),
        )
        return urls + super(RouterAdmin, self).get_urls()


@admin.register(models.Vrf)
class VrfAdmin(admin.ModelAdmin):
    readonly_fields = ('router',)

    def has_add_permission(self, request):
        return False


@admin.register(models.Route)
class RouteAdmin(admin.ModelAdmin):
    readonly_fields = ('vrf',)

    def has_add_permission(self, request):
        return False


class Layer3InterfaceInline(admin.StackedInline):
    model = models.Layer3Interface


@admin.register(models.Vlan)
class VlanAdmin(admin.ModelAdmin):
    readonly_fields = ('router',)
    # inlines = [
    #     Layer3InterfaceInline,
    # ]

    def has_add_permission(self, request):
        return False


class SubInterfaceInline(admin.TabularInline):
    model = models.SubInterface
    fields = ('name', 'type', 'layer_3_interface', 'description', 'notes')
    readonly_fields = ('layer_3_interface', 'notes')


@admin.register(models.PhysicalInterface)
class PhysicalInterfaceAdmin(admin.ModelAdmin):
    readonly_fields = ('router',)
    inlines = [
        SubInterfaceInline,
    ]

    def has_add_permission(self, request):
        return False
