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


class CreateProject(base.Scenario):
    """Creates a new project.

    Configuration:

    * name_prefix: prefix to affix to generated project names
    * max_projects_per_user: maximum projects to create per user before a
      noop is returned
    """

    TYPE = 'CreateProject'

    ALL_CONFIG_PROPS = (
        NAME_PREFIX, MAX_PROJECTS_PER_USER,
    ) = (
        'name_prefix', 'max_projects_per_user',
    )

    DEFAULT_MAX_PROJECTS = 5

    def run(self, user):

        # Sanity check to skip this scenario if no more projects can be created
        max_projects = self.config.get(self.MAX_PROJECTS_PER_USER,
                                       self.DEFAULT_MAX_PROJECTS)
        if len(user.api.projects.list()) >= max_projects:
            msg = 'The user is already at the maximum number of projects [%s]'
            raise base.NoOperation(msg % max_projects)

        # Generate the project name
        name_prefix = self.config.get(self.NAME_PREFIX, 'inn-')
        project_name = name_prefix + base.random_name()

        LOG.debug('Creating project [%s]' % project_name)
        user.api.projects.create(project_name)


class CreateService(base.Scenario):
    """Creates a new service.

    Configuration:

    * name_prefix: prefix to affix to generated service names
    * image_list: comma-separated list of image names to randomly choose from
      when creating the service
    * max_services_per_user: maximum number of services to deploy for each
      user; if this scenario is called and the number of services is at the
      max, no action will be taken
    """

    TYPE = 'CreateService'

    ALL_CONFIG_PROPS = (
        NAME_PREFIX, IMAGE_LIST, MAX_SERVICES
    ) = (
        'name_prefix', 'image_list', 'max_services_per_user'
    )

    DEFAULT_MAX_SERVICES = 5

    # TODO: Add configuration properties for route creation (bool, port, etc.)

    def validate(self):
        super(CreateService, self).validate()
        # Add validation for required config and their values

    def run(self, user):

        # Randomly select a project before looking fro services
        project_name = base.select_random_project(user)

        # Sanity check to skip this scenario if no more services can be created
        max_services = self.config.get(self.MAX_SERVICES,
                                       self.DEFAULT_MAX_SERVICES)
        if len(user.api.services.list()) >= max_services:
            msg = 'The user is already at the maximum service count of [%s]'
            raise base.NoOperation(msg % max_services)

        # Randomly select an image
        image_name = self._select_random_image()

        # Generate the service name
        name_prefix = self.config.get(self.NAME_PREFIX, 'inn-')
        service_name = name_prefix + base.random_name()

        LOG.debug('Creating service [%s] in project [%s] with image [%s]' %
                  (service_name, project_name, image_name))
        user.api.services.create_from_image(service_name,
                                            image_name,
                                            project_name=project_name)

    @property
    def _select_random_image(self):
        il = self.config[self.IMAGE_LIST].split(',')
        image_name = random.choice(il)
        return image_name
