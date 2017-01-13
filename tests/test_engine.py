# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import base

import mock

from innervate.engine import InnervateEngine
from innervate.scenarios.base import NoOperation


class InnervateEngineTests(base.BaseTestCase):

    def setUp(self):
        super(InnervateEngineTests, self).setUp()

        self.engine = InnervateEngine(self.config)
        self.engine.initialize()

    def test_run_random_scenario(self):
        # Setup
        mock_1, mock_2 = mock.MagicMock(), mock.MagicMock()
        mock_user = mock.MagicMock()
        self.engine.scenario_manager.scenarios = [mock_1, mock_2]

        # Test
        self.engine.run_random_scenario(mock_user)

        # Verify
        self.assertTrue(bool(mock_1.run.call_count > 0) ^
                        bool(mock_2.run.call_count > 0))
        if mock_1.run.call_count:
            mock_1.run.assert_called_once_with(mock_user)
        if mock_2.run.call_count:
            mock_2.run.assert_called_once_with(mock_user)

    @mock.patch('innervate.engine.InnervateEngine._choose_scenario')
    def test_run_random_scenario_with_noop(self, mock_choose):
        # Setup
        mock_1, mock_2 = mock.MagicMock(), mock.MagicMock()
        mock_1.run.side_effect = NoOperation()

        self.engine.scenario_manager.scenarios.extend([mock_1, mock_2])
        mock_choose.side_effect = [mock_1, mock_2]

        mock_user = mock.MagicMock()

        # Test
        self.engine.run_random_scenario(mock_user)

        # Verify
        mock_1.run.assert_called_once_with(mock_user)
        mock_2.run.assert_called_once_with(mock_user)
