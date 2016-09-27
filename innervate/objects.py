# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import pykube.objects
from pykube.objects import (  # noqa
    ConfigMap,
    DaemonSet,
    Deployment,
    Endpoint,
    Event,
    HorizontalPodAutoscaler,
    Ingress,
    Job,
    Namespace,
    Node,
    PetSet,
    ReplicaSet,
    ResourceQuota,
    Secret,
    ServiceAccount,
    ThirdPartyResource,
    APIObject,
    NamespacedAPIObject)


class OpenShiftAPIObject(APIObject):
    version = 'v1'
    base = '/oapi'


class OpenShiftNamespacedAPIObject(NamespacedAPIObject):
    version = 'v1'
    base = '/oapi'


class Project(OpenShiftAPIObject):
    endpoint = 'projects'
    kind = 'Project'

    @classmethod
    def new(cls, api, name):
        doc = {
            'apiVersion': 'v1',
            'kind': cls.kind,
            'metadata': {
                'name': name,
                'namespace': None,
            }
        }
        return cls(api, doc)


class ProjectRequest(OpenShiftAPIObject):
    endpoint = 'projectrequests'
    kind = 'ProjectRequest'

    @classmethod
    def new(cls, api, name):
        doc = {
            'apiVersion': 'v1',
            'kind': cls.kind,
            'metadata': {
                'name': name,
                'namespace': None,
            }
        }
        return cls(api, doc)


class DeploymentConfig(OpenShiftNamespacedAPIObject):
    endpoint = 'deploymentconfigs'
    kind = 'DeploymentConfig'

    @classmethod
    def new(cls, api, name, project_name, image_name,
            replicas=1, port=8080, protocol='TCP'):
        doc = {
            'apiVersion': 'v1',
            'kind': cls.kind,
            'metadata': {
                'name': name,
                'namespace': project_name,
                'labels': {
                    'app': name,
                },
            },
            'spec': {
                'replicas': replicas,
                'selector': {
                    'app': name,
                    'deploymentconfig': name,
                },
                'strategy': {
                    'resources': {},
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': name,
                            'deploymentconfig': name,
                        }
                    },
                    'spec': {
                        'containers': [
                            {
                                'image': image_name,
                                'name': name,
                                'ports': [
                                    {
                                        'containerPort': port,
                                        'protocol': protocol,
                                    }
                                ],
                                'resources': {},
                            }
                        ]
                    }
                },
            },
            'status': {}
        }
        return cls(api, doc)


class Service(pykube.objects.Service):

    @classmethod
    def new(cls, api, name, project_name, dc_name, ports=None):
        ports = ports or []

        doc = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': name,
                'namespace': project_name,
            },
            'spec': {
                'ports': [],
                'selector': {
                    'app': dc_name,
                    'deploymentconfig': dc_name,
                }
            },
        }

        for p in ports:
            port_desc = {
                'name': '%s-%s' % (p[0], p[1].lower()),
                'port': p[0],
                'protocol': p[1],
                'targetPort': p[0],
            }
            doc['spec']['ports'].append(port_desc)

        return cls(api, doc)


class Route(OpenShiftNamespacedAPIObject):
    endpoint = 'routes'
    kind = 'Route'

    @classmethod
    def new(cls, api, name, project_name, service_name, port_name):
        doc = {
            'apiVersion': 'v1',
            'kind': cls.kind,
            'metadata': {
                'name': name,
                'namespace': project_name,
            },
            'spec': {
                'port': {
                    'targetPort': port_name,
                },
                'to': {
                    'kind': '',
                    'name': service_name,
                }
            },
            'status': {
                'ingress': None,
            }
        }
        return cls(api, doc)


class ReplicationController(pykube.objects.ReplicationController):

    @classmethod
    def new(cls, api, name, project_name):
        doc = {
            'apiVersion': 'v1',
            'kind': cls.kind,
            'metadata': {
                'name': name,
                'namespace': project_name,
            }
        }
        return cls(api, doc)


class Pod(pykube.objects.Pod):

    @classmethod
    def new(cls, api, name, project_name):
        doc = {
            'apiVersion': 'v1',
            'kind': cls.kind,
            'metadata': {
                'name': name,
                'namespace': project_name
            }
        }
        return cls(api, doc)
