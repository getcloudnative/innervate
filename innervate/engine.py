# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import logging

from innervate.user import UserManager
from innervate.scenario.manager import ScenarioManager


LOG = logging.getLogger(__name__)


class InnervateEngine(object):
    """Driving engine for running the simulations."""

    def __init__(self, config):
        super(InnervateEngine, self).__init__()

        self.config = config

        self.user_manager = None
        self.scenario_manager = None

    def initialize(self):
        LOG.info('Initializing InnervateEngine')

        # Create the manager responsible for tracking and authenticating users
        self.user_manager = UserManager(self.config.host,
                                        self.config.port)

        # Load each configured user
        for u in self.config.users:
            self.user_manager.load_user(u[0], u[1])

        # Create and initialize the scenarios to be run
        self.scenario_manager = ScenarioManager(self.config.scenarios)
