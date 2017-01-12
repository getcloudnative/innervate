# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import logging
import random
import time

from innervate.user import UserManager
from innervate.scenario import ScenarioManager


LOG = logging.getLogger('innervate_engine')


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
        self.scenario_manager = ScenarioManager()
        self.scenario_manager.load(self.config.scenarios)

    def run(self):

        try:
            while True:
                sleep_min, sleep_max = self.config.scenario_sleep_range
                sleep_for = random.randint(sleep_min, sleep_max)

                # Do something
                LOG.info('Running scenario')
                LOG.info('Sleeping for [%s] before next scenario is run' % sleep_for)
                time.sleep(sleep_for)

        except KeyboardInterrupt:
            # Gracefully exit
            self.stop()

    def stop(self):
        LOG.info('Shutting down InnervateEngine')

