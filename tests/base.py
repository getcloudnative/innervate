# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import os
import unittest

import mock

from innervate.config import InnervateConfig


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()

        # Load and initialize the configuration based on the example.yaml
        # This may need to be an explicit testing config in the future, but
        # for now it works until it doesn't
        self.config = InnervateConfig()
        self.config.load(self.example_config_filename)

        # Suitable for mocking out API calls scoped to a user
        self.mock_api = mock.MagicMock()
        self.mock_user = mock.MagicMock()
        self.mock_user.api = self.mock_api

    @property
    def example_config_filename(self):
        x = os.path.dirname(os.path.abspath(__file__))
        ex = os.path.join(os.path.split(x)[0], 'config', 'example.yaml')
        return ex
