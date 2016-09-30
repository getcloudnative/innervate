# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import random

from .create import CreateService


SCENARIO_CLASSES = {
    'CreateService': CreateService,
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
            self.scenarios.append(scenario)

    def run_random_scenario(self, user):
        if not self.scenarios:
            raise Exception('Scenarios must be loaded using the "initialize" call')

        scenario = random.choice(self.scenarios)
        scenario.run(user)
