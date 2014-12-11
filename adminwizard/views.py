from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.options import TO_FIELD_VAR, IS_POPUP_VAR
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http.response import Http404
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _


class AdminWizardView(object):
    template_name = 'adminwizard/change_form.html'

    def dispatch(self, request, *args, **kwargs):
        admin = kwargs['admin']
        object_id = kwargs['object_id']
        form_url = kwargs['form_url']
        extra_context = kwargs['extra_context']

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not admin.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = admin.model
        opts = model._meta
        add = object_id is None
        change = not add

        if add:
            if not admin.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = admin.get_object(request, unquote(object_id))

            if not admin.has_change_permission(request, obj):
                raise PermissionDenied

            if obj is None:
                raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                    'name': force_text(opts.verbose_name), 'key': escape(object_id)})

            if request.method == 'POST' and "_saveasnew" in request.POST:
                return admin.add_view(request, form_url=reverse('admin:%s_%s_add' % (
                    opts.app_label, opts.model_name),
                    current_app=admin.admin_site.name))

        context = dict(admin.admin_site.each_context())

        context.update(extra_context or {})
        app_label = opts.app_label
        preserved_filters = admin.get_preserved_filters(request)
        form_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, form_url)
        view_on_site_url = admin.get_view_on_site_url(obj)
        is_popup = (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET)
        has_add_permission = admin.has_add_permission(request)
        has_change_permission = admin.has_change_permission(request, obj)
        has_delete_permission = admin.has_delete_permission(request, obj)
        save_as = admin.save_as
        context.update({
            'modeladmin': admin,
            'title': (_('Add %s') if add else _('Change %s')) % force_text(opts.verbose_name),
            # adminform=adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': is_popup,
            'to_field': to_field,
            # media=media,
            # inline_admin_formsets=inline_formsets,
            # errors=helpers.AdminErrorList(form, formsets),
            'preserved_filters': admin.get_preserved_filters(request),
            'add': add,
            'change': change,
            'has_add_permission': has_add_permission,
            'has_change_permission': has_change_permission,
            'has_delete_permission': has_delete_permission,
            'has_file_field': True,  # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': view_on_site_url is not None,
            'absolute_url': view_on_site_url,
            'form_url': form_url,
            'opts': opts,
            # 'content_type_id': get_content_type_for_model(admin.model).pk,
            'save_as': save_as,
            'save_on_top': admin.save_on_top,
            'to_field_var': TO_FIELD_VAR,
            'is_popup_var': IS_POPUP_VAR,
            'app_label': app_label,
            'show_delete_link': not is_popup and has_delete_permission and change,
            'show_save_as_new': not is_popup and change and save_as,
            'show_save_and_add_another': has_add_permission and not is_popup and (not save_as or add),
            'show_save_and_continue': not is_popup and has_change_permission,
            'show_save': getattr(admin, 'show_save', True),
        })

        self.admin_context = context
        return super(AdminWizardView, self).dispatch(request)

    def get_context_data(self, form, **kwargs):
        kwargs.update(self.admin_context)
        return super(AdminWizardView, self).get_context_data(form, **kwargs)

    def get_form_initial(self, step):
        if self.admin_context['change']:
            if step is None:
                step = self.steps.current
            form_class = self.form_list[step]
            data = model_to_dict(self.admin_context['original'])
            form = form_class(data=data)
            if form.is_valid():
                return form.cleaned_data
        return {}

    def done(self, form_list, **kwargs):
        modeladmin = self.admin_context['modeladmin']
        form = self.get_bound_form()
        new_object = self.save(form)
        if self.admin_context['add']:
            modeladmin.log_addition(self.request, new_object)
            return modeladmin.response_add(self.request, new_object)
        else:
            formsets, inline_instances = modeladmin._create_formsets(self.request, new_object)
            change_message = modeladmin.construct_change_message(self.request, form, formsets)
            modeladmin.log_change(self.request, new_object, change_message)
            return modeladmin.response_change(self.request, new_object)

    def get_bound_form(self):
        cleaned_data = self.get_all_cleaned_data()
        form_class = self.admin_context['modeladmin'].form
        return form_class(cleaned_data, instance=self.admin_context['original'])

    def save(self, form):
        assert form.is_valid()
        return form.save()
