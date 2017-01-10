# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import copy
import logging
import random

from scenarios import (base, create, delete)


SCENARIO_CLASSES = {
    create.CreateProject.TYPE: create.CreateProject,
    create.CreateService.TYPE: create.CreateService,
    delete.DeleteProject.TYPE: delete.DeleteProject,
    delete.DeleteService.TYPE: delete.DeleteService,
}

LOG = logging.getLogger(__name__)


class ScenarioManager(object):

    def __init__(self):
        super(ScenarioManager, self).__init__()
        self.scenario_classes = copy.copy(SCENARIO_CLASSES)
        self.scenarios = []

    def load(self, config):
        """Loads the configurations for each scenario to be run.

        Each entry in the config will be a dict containing:

        * name: (required) the unique name of the scenario
        * type: (required) the type of scenario being run; this will correspond
          to one of the scenario classes in this package
        * config: dictionary with keys specific to the type of scenario
          being run

        :param config: list of dictionaries describing the scenarios to run
        """
        for scenario_desc in config:
            if 'type' not in scenario_desc:
                raise Exception('Each scenario must contain a "type"')

            type_name = scenario_desc['type']
            name = scenario_desc['name']
            config = scenario_desc.get('config', {})

            scenario = self._instantiate_scenario(name, type_name, config)

            try:
                scenario.validate()
            except base.ValidationException as e:
                LOG.error('Scenario [%s] has an invalid configuration: %s' %
                          (scenario.name, e.message))
                continue
            except Exception as e:
                LOG.error('Scenario [%s] failed validation with an '
                          'unexpected error: %s' % (scenario.name, e.message))
                continue

            self.scenarios.append(scenario)

    def run_random_scenario(self, user):
        """Attempt to run a random scenario.

        If the chosen scenario reports that it does not run, remove it from
        the possibilities and try again with another random scenario. Once
        all of those options have been exhausted, simply exit. I might need
        to change that behavior in the future, but for now it is simply logged.
        """
        if not self.scenarios:
            raise Exception('Scenarios must be loaded using '
                            'the "initialize" call')

        execution_scenarios = copy.copy(self.scenarios)
        while execution_scenarios:
            scenario = self._choose_scenario(execution_scenarios)
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
            LOG.info('No scenarios found to execute for user [%s]' % user)

    def scenario_by_name(self, name):
        # This won't usually be called and the rest of the methods are
        # simpler using a list instead of a dict, so I'm not too worried about
        # the comprehension annoyance here.
        matching = [s for s in self.scenarios if s.name == name]
        if matching:
            return matching[0]
        else:
            return None

    def _instantiate_scenario(self, name, type_name, config):
        scenario_class = self.scenario_classes.get(type_name, None)
        if scenario_class is None:
            raise Exception('Scenario type must be one of "%s"' %
                            ','.join(self.scenario_classes.keys()))

        scenario = scenario_class(name, config)
        return scenario

    @staticmethod
    def _choose_scenario(scenarios):
        return random.choice(scenarios)
