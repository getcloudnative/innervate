# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import abc
import logging


LOG = logging.getLogger(__name__)


class Scenario(object):

    def __init__(self, name, config):
        self.name = name
        self.config = config

        LOG.info('Loaded scenario "%s (%s)" with config: %s' %
                 (self.name, self.__class__.__name__, self.config))

    def __str__(self):
        return '[%s] %s' % (self.__class__.__name__, self.name)

    @abc.abstractmethod
    def run(self, user):
        pass


class NoOperation(Exception):
    """Raised by a scenario when it is requested to run but, because of its
    configuration or the state of the user, the scenario takes no action.
    This is not necessarily an error condition."""
    pass
