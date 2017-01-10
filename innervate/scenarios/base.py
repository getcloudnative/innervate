# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import abc
import logging
import random
import string


LOG = logging.getLogger(__name__)

RANDOM_NAME_LENGTH = 8


class Scenario(object):

    ALL_CONFIG_PROPS = []

    def __init__(self, name, config):
        self.name = name
        self.config = config

        LOG.debug('Loaded scenario "%s (%s)" with config: %s' %
                  (self.name, self.__class__.__name__, self.config))

    def __str__(self):
        return '[%s] %s' % (self.__class__.__name__, self.name)

    def validate(self):
        """Run when a scenario is loaded, this call should ensure the required configuration
        is present and valid.

        :raises ValidationException: if any of the scenario configuration is invalid
        """
        invalid_keys = [x for x in self.config.keys() if x not in self.ALL_CONFIG_PROPS]
        if invalid_keys:
            raise ValidationException('Invalid keys [%s]' % ','.join(invalid_keys))

    @abc.abstractmethod
    def run(self, user):
        pass


class ScenarioRunReport(object):
    """Describes the result of a single scenario execution.

    This might be overkill, but I wanted a way for the engine to control
    the logging of what actions it performs. I didn't like the idea of
    simply returning a string from the scenario.run method, so this is
    a very light wrapper with some more programmatically accessible
    fields.
    """

    def __init__(self, msg, project_name=None, service_name=None):
        super(ScenarioRunReport, self).__init__()
        self.msg = msg
        self.project_name = project_name
        self.service_name = service_name


class NoOperation(Exception):
    """Raised by a scenario when it is requested to run but, because of its
    configuration or the state of the user, the scenario takes no action.
    This is not necessarily an error condition."""
    pass


class ValidationException(Exception):
    """Raised when a scenario has an invalid configuration."""
    pass


def select_random_project(user):
    project_names = [p.name for p in user.api.projects.list()]

    if not project_names:
        raise NoOperation('The user [%s] has no existing projects' % user.username)

    project_name = random.choice(project_names)
    user.api.current_project = project_name

    return project_name


def random_name():
    """Returns a suitable randomized name."""
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(RANDOM_NAME_LENGTH))
