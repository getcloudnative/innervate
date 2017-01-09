# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import os
import unittest

from innervate.config import InnervateConfig
from innervate.engine import InnervateEngine


class BaseFunctionalTestCase(unittest.TestCase):

    def setUp(self):
        super(BaseFunctionalTestCase, self).setUp()

        # Load and initialize the configuration based on the example.yaml
        # This may need to be an explicit testing config in the future, but
        # for now it works until it doesn't
        self.config = InnervateConfig()
        self.config.load(self.example_config_filename)

        # Create and initialize an engine but don't start the loop; it
        # will be used to get to the configured pieces we need
        self.engine = InnervateEngine(self.config)
        self.engine.initialize()

        # Shortcut variables
        self.user = self.engine.user_manager.user('user1')

    def scenario(self, name):
        return self.engine.scenario_manager.scenario_by_name(name)

    @property
    def example_config_filename(self):
        x = os.path.dirname(os.path.abspath(__file__))
        ex = os.path.join(os.path.split(x)[0], 'config', 'example.yaml')
        return ex
