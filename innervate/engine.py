# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import copy
import logging
import random
from scenarios import base
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

                LOG.info('-' * 20)
                user = self.user_manager.random_user()
                self.run_random_scenario(user)
                LOG.info('-' * 20)

                LOG.info('Sleeping for [%s] before next scenario is run' % sleep_for)
                time.sleep(sleep_for)

        except KeyboardInterrupt:
            # Gracefully exit
            self.stop()

    def run_random_scenario(self, user):
        """Attempt to run a random scenario.

        If the chosen scenario reports that it does not run, remove it from
        the possibilities and try again with another random scenario. Once
        all of those options have been exhausted, simply exit. I might need
        to change that behavior in the future, but for now it is simply logged.
        """
        execution_scenarios = copy.copy(self.scenario_manager.scenarios)
        while execution_scenarios:
            scenario = self._choose_scenario(execution_scenarios)
            try:
                result = scenario.run(user)
                LOG.info(result.msg)
            except base.NoOperation as e:
                # Remove this scenario from the possible scenarios and attempt to
                # try another
                LOG.info('Skipping scenario [%s]: %s' % (scenario.name, e.message))
                execution_scenarios.remove(scenario)
            else:
                break
        else:
            # We ran out of scenarios and none executed. This isn't an error per se, but
            # it likely means that without user intervention, subsequent attempts to
            # run the scenario set again will not produce any results.
            LOG.info('No scenarios found to execute for user [%s]' % user)

    @staticmethod
    def _choose_scenario(scenarios):
        return random.choice(scenarios)

    def stop(self):
        LOG.info('Shutting down InnervateEngine')



