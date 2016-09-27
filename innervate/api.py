# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import time

from innervate.objects import Project, ProjectRequest, Service, \
    DeploymentConfig, Route, ReplicationController


class OpenShiftAPI(object):

    def __init__(self, user):
        super(OpenShiftAPI, self).__init__()
        self.user = user

    def list_project_names(self):
        projects_data = Project.objects(self.user.http_client)
        names = [p.name for p in projects_data]
        return names

    def create_project(self, project_name):
        p = ProjectRequest.new(self.user.http_client, project_name)
        p.create()

    def delete_project(self, project_name):
        p = Project.new(self.user.http_client, project_name)
        p.delete()

    def list_service_names(self, project_name):
        service_data = Service.objects(self.user.http_client).filter(namespace=project_name)
        names = [p.name for p in service_data]
        return names

    def get_service(self, project_name, service_name):
        query = Service.objects(self.user.http_client)
        query.namespace = project_name
        service_data = query.get_by_name(service_name)
        return service_data

    def create_service_from_image(self, project_name, service_name,
                                  image_name, ports=None,
                                  create_route=True):
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

    def delete_service(self, project_name, service_name):
        # dc = DeploymentConfig.new(self.user.http_client, service_name,
        #                          project_name, None, replicas=0)
        query = DeploymentConfig.objects(self.user.http_client)
        query.namespace = project_name
        dc = query.get_by_name(service_name)
        dc.obj['spec']['replicas'] = 0
        dc.update()

        time.sleep(5)  # probably a better way to handle this

        s = Service.new(self.user.http_client, service_name, project_name,
                        service_name)
        s.delete()
        dc.delete()

        rc_names = self.get_replication_controller_names_for_service(project_name, service_name)
        for r in rc_names:
            rc = ReplicationController.new(self.user.http_client, r, project_name)
            rc.delete()

        route_names = self.get_route_names_for_service(project_name, service_name)
        for r in route_names:
            route = Route.new(self.user.http_client, r, project_name, service_name, None)
            route.delete()

    def get_replication_controller_names_for_service(self, project_name, service_name):
        rc_data =\
            ReplicationController.objects(self.user.http_client).filter(namespace=project_name,
                                                                        selector={'app': service_name})
        names = [r.name for r in rc_data]
        return names

    def get_route_names_for_service(self, project_name, service_name):
        selector = {'app': service_name}
        route_data = Route.objects(self.user.http_client).filter(namespace=project_name,
                                                                 selector=selector)
        names = [r.name for r in route_data]
        return names

