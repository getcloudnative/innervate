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


class ScaleScenario(base.Scenario):
    """Base functionality for scaling a service. """

    def __init__(self, name, weight, config, f_test, f_adjust):
        super(ScaleScenario, self).__init__(name, weight, config)

        self.f_test = f_test
        self.f_adjust = f_adjust

    def run(self, user):

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

                if self.f_test(current_count):
                    new_count = self.f_adjust(current_count)
                    user.api.services.scale(s, new_count, project_name=p)
                    msg = 'Scaled service [%s] in project [%s] to ' \
                          '[%s] pods' % (s, p, new_count)
                    return base.ScenarioRunReport(msg,
                                                  project_name=p,
                                                  service_name=s)
        else:
            # If we got here, no projects had any services that could be
            # scaled, so this is a noop
            raise base.NoOperation('No services eligible for scaling')


class ScaleUp(ScaleScenario):
    """Scales a service up.

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

    def __init__(self, name, weight, config):
        max_pods = config.get(self.MAX_PODS, self.DEFAULT_MAX_PODS)

        def test(x): return x < max_pods

        def change(x): return x + 1

        super(ScaleUp, self).__init__(name, weight, config, test, change)


class ScaleDown(ScaleScenario):
    """Scales a service down (but not to zero)."""

    TYPE = 'ScaleDown'

    def __init__(self, name, weight, config):

        def test(x): return x > 0

        def change(x): return x - 1

        super(ScaleDown, self).__init__(name, weight, config, test, change)

