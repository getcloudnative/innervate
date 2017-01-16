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

        # Log the state of the configured engine
        LOG.info('Engine Configuration:')
        LOG.info('Users:')
        for u in self.user_manager.iterator():
            LOG.info('  %s' % u.username)
        LOG.info('Scenarios:')
        for s in self.scenario_manager.iterator():
            LOG.info('  %s :: Type: %s :: Weight: %s' %
                     (s.name, s.TYPE, s.weight))
        LOG.info('=' * 20)

    def run(self):

        try:
            counter = 0
            while True:
                sleep_min, sleep_max = self.config.scenario_sleep_range
                sleep_for = random.randint(sleep_min, sleep_max)

                # Log the state before running the scenario in case the
                # scenario is a delete; there is a possible race condition
                # where the deleted project will appear in the list but
                # not be accessible when looking up the services (because it's
                # in the process of being deleted), so it's simpler to log
                # it now and not even worry about it.
                if (self.config.log_state_every and
                        counter % self.config.log_state_every == 0):
                    LOG.info('Current State:')
                    self.log_current_state()
                counter += 1

                LOG.info('-' * 20)

                while True:
                    execution_users = copy.copy(self.user_manager.all_users)
                    try:
                        user = self._choose_user(execution_users)
                        LOG.info('Running scenario for user [%s]' %
                                 user.username)
                        self.run_random_scenario(user)
                        break
                    except NoScenariosExecuted:
                        # Nothing to do for this user, try another
                        LOG.info('No scenarios were able to be executed by'
                                 'user [%s]' % user.username)
                        execution_users.remove(user)
                else:
                    # The break was never hit, which meant there was nothing
                    # done. This shouldn't happen unless there is a grossly
                    # misconfigured set of scenarios
                    LOG.info('No users were able to execute any scenarios')

                LOG.info('-' * 20)

                LOG.info('Sleeping for %s seconds before the next scenario '
                         'is run' % sleep_for)
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
        execution_scenarios = self._expand_scenarios()
        skipped_scenario_names = []
        while execution_scenarios:
            scenario = self._choose_scenario(execution_scenarios)

            if scenario.name in skipped_scenario_names:
                continue

            try:
                result = scenario.run(user)
                LOG.info(result.msg)
            except base.NoOperation as e:
                # The scenario might appear multiple times depending on the
                # weights assigned, so keep track of ones we've skipped in
                # the past and try another
                LOG.info('Skipping scenario [%s]: %s' % (scenario.name,
                                                         e.message))
                skipped_scenario_names.append(scenario.name)

            else:
                break
        else:
            # We ran out of scenarios and none executed. This isn't an error
            # per se, but it likely means that without user intervention,
            # subsequent attempts to run the scenario set again will not
            # produce any results.
            LOG.info('No scenarios found to execute for user [%s]' % user)
            raise NoScenariosExecuted()

    def _expand_scenarios(self):
        """Creates a copy of the scenarios list and applies the scenario
        weights."""
        scenarios = []
        for s in self.scenario_manager.iterator():
            scenarios.extend([s for x in range(0, s.weight)])
        return scenarios

    @staticmethod
    def _choose_scenario(scenarios):
        # Wrapper method to ease mocking in tests
        return random.choice(scenarios)

    @staticmethod
    def _choose_user(users):
        # Wrapper method to ease mocking in tests
        return random.choice(users)

    def log_current_state(self):
        """Logs the current state of each user's projects."""

        for u in self.user_manager.iterator():
            LOG.info('User: %s' % u.username)

            u_projects = u.api.projects.list()
            for p in u_projects:
                LOG.info('  Project: %s' % p.name)

                services = u.api.services.list(project_name=p.name)
                for s in services:
                    replicas = u.api.services.get_replica_count(
                        s.name, project_name=p.name)
                    LOG.info('    Service: %s (Count: %s)' %
                             (s.name, replicas))

    def cleanup(self):
        """Deletes all projects for each configured user."""

        LOG.info('Cleaning up user accounts')
        for u in self.user_manager.iterator():
            LOG.info('User: %s' % u.username)

            u_projects = u.api.projects.list()
            for p in u_projects:
                LOG.info('  Deleting Project: %s' % p.name)
                u.api.projects.delete(p.name)

        while True:
            LOG.info('Waiting for projects to be deleted...')
            total_projects = 0
            for u in self.user_manager.iterator():
                u_projects = u.api.projects.list()
                total_projects += len(u_projects)

            if total_projects == 0:
                LOG.info('Project clean up complete')
                break
            else:
                time.sleep(5)

    def stop(self):
        LOG.info('Shutting down InnervateEngine')
        LOG.info('Auto Clean: %s' % self.config.auto_clean)
        if self.config.auto_clean:
            self.cleanup()


class NoScenariosExecuted(Exception):
    pass
