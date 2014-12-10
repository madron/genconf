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


def save_objects(objects):
    save_instances(
        objects.get('router', []),
        fixed_fields=['project'],
        search_fields=['name']
    )
    save_instances(
        objects.get('vrf', []),
        fixed_fields=['router'],
        search_fields=['name']
    )
    save_instances(
        objects.get('route', []),
        fixed_fields=['vrf'],
        search_fields=['network', 'next_hop']
    )
    save_instances(
        objects.get('vlan', []),
        fixed_fields=['router'],
        search_fields=['tag']
    )
    save_instances(
        objects.get('physicalinterface', []),
        fixed_fields=['router'],
        search_fields=['name']
    )


def get_physical_interfaces(objects, router, type=None, layer=None):
    interfaces = [i for i in objects['physicalinterface'] if i.router == router]
    if type:
        interfaces = [i for i in interfaces if i.type == type]
    if layer:
        interfaces = [i for i in interfaces if i.layer == layer]
    return interfaces
