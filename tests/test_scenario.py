# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import base

import mock

from innervate import scenario
from innervate.scenarios import base as scenario_base


class ScenarioManagerTests(base.BaseTestCase):

    def setUp(self):
        super(ScenarioManagerTests, self).setUp()

        self.manager = scenario.ScenarioManager()

    @mock.patch('innervate.scenario.ScenarioManager._instantiate_scenario')
    def test_load(self, mock_inst):
        # Setup
        mock_1 = mock.MagicMock()
        mock_2 = mock.MagicMock()
        mock_inst.side_effect = [mock_1, mock_2]

        # Test
        self.manager.load(self._scenarios_config())

        # Verify
        mock_1.validate.assert_called_once()
        mock_2.validate.assert_called_once()

        self.assertEqual([mock_1, mock_2], self.manager.scenarios)

    @mock.patch('innervate.scenario.ScenarioManager._instantiate_scenario')
    def test_load_validate_fail(self, mock_inst):
        # Setup
        mock_1 = mock.MagicMock()
        mock_2 = mock.MagicMock()
        mock_inst.side_effect = [mock_1, mock_2]

        mock_2.validate.side_effect = scenario_base.ValidationException()

        # Test
        self.manager.load(self._scenarios_config())

        # Verify
        mock_1.validate.assert_called_once()
        mock_2.validate.assert_called_once()

        self.assertEqual([mock_1], self.manager.scenarios)

    @mock.patch('innervate.scenario.ScenarioManager._instantiate_scenario')
    def test_load_unexpected_fail(self, mock_inst):
        # Setup
        mock_1 = mock.MagicMock()
        mock_2 = mock.MagicMock()
        mock_inst.side_effect = [mock_1, mock_2]

        mock_2.validate.side_effect = Exception()

        # Test
        self.manager.load(self._scenarios_config())

        # Verify
        mock_1.validate.assert_called_once()
        mock_2.validate.assert_called_once()

        self.assertEqual([mock_1], self.manager.scenarios)

    def test_run_random_scenario(self):
        # Setup
        mock_1, mock_2 = mock.MagicMock(), mock.MagicMock()
        mock_user = mock.MagicMock()
        self.manager.scenarios.extend([mock_1, mock_2])

        # Test
        self.manager.run_random_scenario(mock_user)

        # Verify
        self.assertTrue(bool(mock_1.run.call_count > 0) ^
                        bool(mock_2.run.call_count > 0))
        if mock_1.run.call_count:
            mock_1.run.assert_called_once_with(mock_user)
        if mock_2.run.call_count:
            mock_2.run.assert_called_once_with(mock_user)

    def test_run_random_scenario_no_load(self):
        self.assertRaises(Exception,
                          self.manager.run_random_scenario, None)

    @mock.patch('innervate.scenario.ScenarioManager._choose_scenario')
    def test_run_random_scenario_with_noop(self, mock_choose):
        # Setup
        mock_1, mock_2 = mock.MagicMock(), mock.MagicMock()
        mock_1.run.side_effect = scenario_base.NoOperation()

        self.manager.scenarios.extend([mock_1, mock_2])
        mock_choose.side_effect = [mock_1, mock_2]

        mock_user = mock.MagicMock()

        # Test
        self.manager.run_random_scenario(mock_user)

        # Verify
        mock_1.run.assert_called_once_with(mock_user)
        mock_2.run.assert_called_once_with(mock_user)

    def test_instantiate_scenario(self):
        # Setup
        class FakeScenarioType(object):
            def __init__(self, name, config):
                self.name = name
                self.config = config

        scenario.SCENARIO_CLASSES.clear()
        scenario.SCENARIO_CLASSES['type1'] = FakeScenarioType

        # Test
        created = self.manager._instantiate_scenario('name1', 'type1', {})

        # Verify
        self.assertTrue(isinstance(created, FakeScenarioType))
        self.assertEqual('name1', created.name)
        self.assertEqual({}, created.config)

    @staticmethod
    def _scenarios_config():
        """Returns a configuration for testing scenarios that is consistent
        with the format returned from the configuration file.

        :return: list of scenario configurations
        :rtype:  [dict]
        """
        scenarios = [
            {'name': 'scenario1',
             'type': 'type1',
             'config': {}},
            {'name': 'scenario2',
             'type': 'type2',
             'config': {}},
        ]
        return scenarios
