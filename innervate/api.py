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

    def __init__(self, user):
        super(OpenShiftAPI, self).__init__()
        self.user = user

        # Used as the default for all namespaced calls
        self.current_project = None

    def list_projects(self):
        return Project.objects(self.user.http_client)

    def create_project(self, project_name):
        p = ProjectRequest.new(self.user.http_client, project_name)
        p.create()

    def delete_project(self, project_name):
        p = Project.new(self.user.http_client, project_name)
        p.delete()

    def list_services(self, project_name=None):
        project_name = project_name or self.current_project
        return Service.objects(self.user.http_client).filter(namespace=project_name)

    def get_service(self, service_name, project_name=None):
        project_name = project_name or self.current_project
        query = Service.objects(self.user.http_client).filter(namespace=project_name)
        return query.get_by_name(service_name)

    def create_service_from_source(self, service_name, source_uri, source_image, source_namespace,
                                   project_name=None, ports=None, create_route=True):
        project_name = project_name or self.current_project

        bc = BuildConfig.new(self.user.http_client, service_name, project_name,
                             source_uri, source_image, source_namespace)
        bc.create()

        image_name = '%s:latest' % service_name
        self.create_service_from_image(service_name,
                                       image_name,
                                       project_name=project_name,
                                       ports=ports,
                                       create_route=create_route)

    def create_service_from_image(self, service_name, image_name,
                                  project_name=None, ports=None, create_route=True):
        project_name = project_name or self.current_project

        dc = DeploymentConfig.new(self.user.http_client, service_name,
                                  project_name, image_name)
        dc.create()

        s = Service.new(self.user.http_client, service_name, project_name,
                        service_name, ports=ports)
        s.create()

        if create_route:
            # This is kinda ghetto, but for now, just grab the
            # first port and use that for the route
            port_name = s.ports[0]['name']

            r = Route.new(self.user.http_client, service_name, project_name,
                          service_name, port_name)
            r.create()

    def delete_service(self, service_name, project_name=None):
        project_name = project_name or self.current_project

        query = DeploymentConfig.objects(self.user.http_client).filter(namespace=project_name)
        dc = query.get_by_name(service_name)
        dc.obj['spec']['replicas'] = 0
        dc.update()

        time.sleep(3)  # probably a better way to handle this :)

        s = Service.new(self.user.http_client, service_name, project_name,
                        service_name)
        s.delete()
        dc.delete()

        rcs = self.list_rc_for_service(service_name, project_name=project_name)
        rc_names = [r.name for r in rcs]
        for r in rc_names:
            rc = ReplicationController.new(self.user.http_client, r, project_name)
            rc.delete()

        routes = self.list_routes_for_service(service_name, project_name=project_name)
        route_names = [r.name for r in routes]
        for r in route_names:
            route = Route.new(self.user.http_client, r, project_name, service_name, None)
            route.delete()

    def list_rc_for_service(self, service_name, project_name=None):
        project_name = project_name or self.current_project

        rc_data =\
            ReplicationController.objects(self.user.http_client).filter(namespace=project_name,
                                                                        selector={'app': service_name})
        return rc_data

    def list_routes_for_service(self, service_name, project_name=None):
        project_name = project_name or self.current_project
        selector = {'app': service_name}
        route_data = Route.objects(self.user.http_client).filter(namespace=project_name,
                                                                 selector=selector)
        return route_data

