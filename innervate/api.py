# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import time

from innervate.objects import Project, ProjectRequest, Service, \
    DeploymentConfig, Route, ReplicationController, BuildConfig


class OpenShiftAPI(object):
    """Aggregator for all of the object-specific API calls."""

    def __init__(self, http_client):
        super(OpenShiftAPI, self).__init__()

        self.http_client = http_client

        # Used as the default for all namespaced calls
        self.current_project = None

        self.projects = ProjectsAPI(self)
        self.services = ServicesAPI(self)


class ProjectsAPI(object):

    def __init__(self, base_api):
        super(ProjectsAPI, self).__init__()
        self.base_api = base_api

    def list(self):
        return Project.objects(self.base_api.http_client)

    def create(self, project_name):
        p = ProjectRequest.new(self.base_api.http_client, project_name)
        p.create()

    def delete(self, project_name):
        p = Project.new(self.base_api.http_client, project_name)
        p.delete()


class ServicesAPI(object):

    def __init__(self, base_api):
        super(ServicesAPI, self).__init__()
        self.base_api = base_api

    def list(self, project_name=None):
        project_name = project_name or self.base_api.current_project
        return Service.objects(self.base_api.http_client).filter(
            namespace=project_name)

    def get(self, service_name, project_name=None):
        project_name = project_name or self.base_api.current_project
        query = Service.objects(self.base_api.http_client).filter(
            namespace=project_name)
        return query.get_by_name(service_name)

    def create_from_source(self, service_name, source_uri,
                           source_image, source_namespace,
                           project_name=None, ports=None, create_route=True):
        project_name = project_name or self.base_api.current_project

        bc = BuildConfig.new(self.base_api.http_client, service_name, project_name,
                             source_uri, source_image, source_namespace)
        bc.create()

        image_name = '%s:latest' % service_name
        self.create_from_image(service_name, image_name,
                               project_name=project_name, ports=ports,
                               create_route=create_route)

    def create_from_image(self, service_name, image_name,
                          project_name=None, ports=None, create_route=True):
        project_name = project_name or self.base_api.current_project

        dc = DeploymentConfig.new(self.base_api.http_client, service_name,
                                  project_name, image_name)
        dc.create()

        s = Service.new(self.base_api.http_client, service_name, project_name,
                        service_name, ports=ports)
        s.create()

        if create_route:
            # This is kinda ghetto, but for now, just grab the
            # first port and use that for the route
            port_name = s.ports[0]['name']

            r = Route.new(self.base_api.http_client, service_name, project_name,
                          service_name, port_name)
            r.create()

    def delete(self, service_name, project_name=None):
        project_name = project_name or self.base_api.current_project

        query = DeploymentConfig.objects(self.base_api.http_client).filter(
            namespace=project_name)
        dc = query.get_by_name(service_name)
        dc.obj['spec']['replicas'] = 0
        dc.update()

        time.sleep(3)  # probably a better way to handle this :)

        s = Service.new(self.base_api.http_client, service_name, project_name,
                        service_name)
        s.delete()
        dc.delete()

        rcs = self.list_rc(service_name, project_name=project_name)
        rc_names = [r.name for r in rcs]
        for r in rc_names:
            rc = ReplicationController.new(self.base_api.http_client, r,
                                           project_name)
            rc.delete()

        routes = self.list_routes(service_name,
                                              project_name=project_name)
        route_names = [r.name for r in routes]
        for r in route_names:
            route = Route.new(self.base_api.http_client, r, project_name,
                              service_name, None)
            route.delete()

    def list_rc(self, service_name, project_name=None):
        project_name = project_name or self.base_api.current_project

        rc_data =\
            ReplicationController.objects(self.base_api.http_client).filter(
                namespace=project_name, selector={'app': service_name})
        return rc_data

    def list_routes(self, service_name, project_name=None):
        project_name = project_name or self.base_api.current_project
        selector = {'app': service_name}
        route_data = Route.objects(self.base_api.http_client).filter(
            namespace=project_name, selector=selector)
        return route_data

    def scale(self, service_name, new_replicas, project_name=None):
        project_name = project_name or self.base_api.current_project
        rc = self.list_rc(service_name, project_name=project_name).get()
        rc.obj['spec']['replicas'] = new_replicas
        rc.update()
