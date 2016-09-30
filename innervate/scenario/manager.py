# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import copy
import logging
import random

from . import (base, create)


LOG = logging.getLogger(__name__)

SCENARIO_CLASSES = {
    'CreateService': create.CreateService,
}


class ScenarioManager(object):

    def __init__(self, config):
        """Loads the configurations for each scenario to be run.

        Each entry in the config will be a dict containing:
        * name: the unique name of the scenario
        * type: the type of scenario being run; this will correspond to one of the
                scenario classes in this package
        * config: dictionary with keys specific to the type of scenario being run

        :param config: list of dictionaries describing the scenarios to run
        """
        self.scenarios = []

        for scenario_desc in config:
            if 'type' not in scenario_desc:
                raise Exception('Each scenario must contain a "type"')

            scenario_class = SCENARIO_CLASSES.get(scenario_desc['type'], None)
            if scenario_class is None:
                raise Exception('Scenario type must be one of "%"' % ','.join(SCENARIO_CLASSES.keys()))

            name = scenario_desc.get('name', None) or scenario_desc['type']
            scenario = scenario_class(name,
                                      scenario_desc.get('config', None))

            try:
                scenario.validate()
            except base.ValidationException as e:
                LOG.error('Scenario [%s] has an invalid configuration: %s' % (scenario.name, e.message))
                continue

            self.scenarios.append(scenario)

    def run_random_scenario(self, user):
        if not self.scenarios:
            raise Exception('Scenarios must be loaded using the "initialize" call')

        # Attempt to run a random scenario. If the scenario reports that it does not
        # run, remove it from the possibilities and try again with another random
        # scenario. Once all of those options have been exhausted,
        execution_scenarios = copy.copy(self.scenarios)
        while execution_scenarios:
            scenario = random.choice(self.scenarios)
            try:
                scenario.run(user)
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
            print('No scenarios found to execute for user [%s]' % user)
