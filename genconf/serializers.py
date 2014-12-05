import json
import netaddr


class ProjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (netaddr.IPAddress, netaddr.IPNetwork)):
            return str(obj)
        return super(ProjectEncoder, self).default(obj)
