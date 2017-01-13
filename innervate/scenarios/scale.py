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


class ScaleUp(base.Scenario):
    """Scales a random service up.

    Configuration:

    * max_pods_per_service: maximum number of pods to scale to
    """

    TYPE = 'ScaleUp'

    ALL_CONFIG_PROPS = (
        MAX_PODS,
    ) = (
        'max_pods_per_service',
    )

    DEFAULT_MAX_PODS = 10

    def run(self, user):
        max_pods = self.config.get(self.MAX_PODS, self.DEFAULT_MAX_PODS)

        # Collect all project names to look through
        project_names = [p.name for p in user.api.projects.list()]

        if not project_names:
            raise base.NoOperation('The user has no existing projects')

        # Check each project (randomly) for a service eligible for scaling
        random.shuffle(project_names)
        for p in project_names:
            service_names = [s.name for s
                             in user.api.services.list(project_name=p)]

            # Punch out if there aren't any deployed services
            if not service_names:
                continue

            # Try each service in this project to see if they are at their
            # maximum pod count. If so, scale it and return
            random.shuffle(service_names)
            for s in service_names:
                current_count = user.api.services.get_replica_count(
                    s, project_name=p)

                if current_count < max_pods:
                    new_count = current_count + 1
                    user.api.services.scale(s, new_count, project_name=p)
                    msg = 'Scaled service [%s] in project [%s] to [%s] pods'
                    return msg % (s, p, new_count)
        else:
            # If we got here, no projects had any services that could be
            # scaled, so this is a noop
            raise base.NoOperation('No services eligible for scaling')







