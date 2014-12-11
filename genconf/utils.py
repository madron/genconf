from operator import attrgetter
from genconf import models


def save_instances(instances, fixed_fields=(), search_fields=()):
    if not instances:
        return
    model_class = type(instances[0])

    # Find fixed field groups
    groups = []
    for instance in instances:
        fixed_filter = dict()
        for field in fixed_fields:
            fixed_filter[field] = getattr(instance, field)
        group = None
        for g in groups:
            if g['fixed_filter'] == fixed_filter:
                group = g
                break
        if not group:
            group = dict(fixed_filter=fixed_filter, instances=[])
            groups.append(group)
        group['instances'].append(instance)

    # Save instances
    used_pks = []
    for group in groups:
        old_objects = model_class.objects.order_by('pk')
        if group['fixed_filter']:
            old_objects = old_objects.filter(**group['fixed_filter'])
        for instance in group['instances']:
            assert(type(instance) == model_class)
            # Trick to force pk assignment
            for field in instance._meta.fields:
                setattr(instance, field.name, getattr(instance, field.name))

            if old_objects.count() > 0:
                search_filter = dict()
                for field in search_fields:
                    search_filter[field]=getattr(instance, field)
                try:
                    old = old_objects.get(**search_filter)
                except model_class.DoesNotExist:
                    old = old_objects[0]
                instance.pk = old.pk

            instance.save()
            old_objects = old_objects.exclude(pk=instance.pk)
            used_pks.append(instance.pk)

    # Delete not needed old objects
    for group in groups:
        old_objects = model_class.objects.order_by('pk')
        if group['fixed_filter']:
            old_objects = old_objects.filter(**group['fixed_filter'])
        old_objects = old_objects.exclude(pk__in=used_pks)
        if old_objects.count() > 0:
            old_objects.delete()


def save_project(project):
    router_keys = project['router'].keys()
    router_keys.sort()
    router_list = []
    vrf_list = []
    route_list = []
    vlan_list = []
    physicalinterface_list = []
    subinterface_list = []
    for router_key in router_keys:
        router = project['router'][router_key]
        router_list.append(router['router_instance'])
        vrf_list += router.get('vrf', [])
        route_list += router.get('route', [])
        vlans = router.get('vlan', dict()).values()
        vlan_list += sorted(vlans, key=attrgetter('tag'))
        physicalinterface_list += router.get('physicalinterface', [])
        subinterface_list += router.get('subinterface', [])
    save_instances(router_list, fixed_fields=['project'], search_fields=['name'])
    save_instances(vrf_list, fixed_fields=['router'], search_fields=['name'])
    save_instances(route_list, fixed_fields=['vrf'], search_fields=['network', 'next_hop'])
    save_instances(vlan_list, fixed_fields=['router'], search_fields=['tag'])
    save_instances(physicalinterface_list, fixed_fields=['router'], search_fields=['name'])
    save_instances(subinterface_list, fixed_fields=['physical_interface'], search_fields=['name'])
    save_instances(
        project.get('physicallink', []),
        fixed_fields=['project'],
        search_fields=['router__name', 'name']
    )


def get_physical_interfaces(router, type=None, layer=None):
    interfaces = router['physicalinterface']
    if type:
        interfaces = [i for i in interfaces if i.type == type]
    if layer:
        interfaces = [i for i in interfaces if i.layer == layer]
    return interfaces
