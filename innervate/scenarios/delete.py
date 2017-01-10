# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import logging
import random

from . import base


LOG = logging.getLogger(__name__)


class DeleteProject(base.Scenario):
    """Deletes a random existing project.

    This scenario will return a noop if the user has no projects deployed.
    """

    TYPE = 'DeleteProject'

    def run(self, user):

        # Sanity check to make sure there's something to actually delete
        all_projects = user.api.projects.list()
        if not all_projects:
            msg = 'There are no projects deployed for the user'
            raise base.NoOperation(msg)

        doomed = self._select_random_project(all_projects)

        LOG.debug('Deleting project [%s]' % doomed.name)
        user.api.projects.delete(doomed.name)

        msg = 'Deleted project [%s]' % doomed.name
        return base.ScenarioRunReport(msg, project_name=doomed.name)

    @staticmethod
    def _select_random_project(all_projects):
        all_projects = [p for p in all_projects]
        project = random.choice(all_projects)
        return project


class DeleteService(base.Scenario):
    """Deletes a random service from a random project.

    This scenario will repeatedly search projects for a service to delete
    until no more projects are found.
    """

    TYPE = 'DeleteService'

    def run(self, user):

        all_projects = user.api.projects.list()
        for p in all_projects:
            proj_services = user.api.services.list(project_name=p.name)
            if len(proj_services) > 0:
                break
        else:
            msg = 'There are no projects containing services'
            raise base.NoOperation(msg)

        doomed = self._select_random_service(proj_services)

        LOG.debug('Deleting service [%s] from project [%s]' %
                  (doomed.name, p.name))
        user.api.services.delete(doomed.name, project_name=p.name)

        msg = 'Deleted service [%s] from project [%s]' % (doomed.name, p.name)
        return base.ScenarioRunReport(msg,
                                      project_name=p.name,
                                      service_name=doomed.name)

    @staticmethod
    def _select_random_service(all_services):
        all_services = [s for s in all_services]
        service = random.choice(all_services)
        return service
