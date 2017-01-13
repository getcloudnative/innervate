# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import base

import mock

from innervate.scenarios import base as scenario_base
from innervate.scenarios import create


class CreateProjectTests(base.BaseTestCase):

    def setUp(self):
        super(CreateProjectTests, self).setUp()

        self.s_config = self.config.scenarios_for_type(
            create.CreateProject.TYPE)[0]['config']
        self.scenario = create.CreateProject('create1', 1, self.s_config)

    def test_run_noop(self):
        # Setup
        configured_max = self.s_config[create.CreateProject.MAX_PROJECTS_PER_USER]
        self.mock_api.projects.list.return_value = [None] * (configured_max + 1)

        # Test
        self.assertRaises(scenario_base.NoOperation,
                          self.scenario.run, self.mock_user)
        self.mock_api.projects.list.assert_called_once_with()

    @mock.patch('innervate.scenarios.base.random_name')
    def test_run(self, mock_name):
        # Setup
        self.mock_api.projects.list.return_value = []
        mock_name.return_value = 'proj1'

        # Test
        report = self.scenario.run(self.mock_user)

        # Verify
        self.assertTrue(isinstance(report, scenario_base.ScenarioRunReport))
        self.assertEqual('inn-proj1', report.project_name)

        self.mock_api.projects.list.assert_called_once_with()
        self.mock_api.projects.create.assert_called_once_with('inn-proj1')


class CreateServiceTests(base.BaseTestCase):

    def setUp(self):
        super(CreateServiceTests, self).setUp()

        self.s_config = self.config.scenarios_for_type(
            create.CreateService.TYPE)[0]['config']
        self.scenario = create.CreateService('create1', 1, self.s_config)

    @mock.patch('innervate.scenarios.base.select_random_project')
    def test_run_noop(self, mock_select):
        # Setup
        mock_select.return_value = 'proj1'

        configured_max = self.s_config[create.CreateService.MAX_SERVICES]
        self.mock_api.services.list.return_value = [None] * (configured_max + 1)

        # Test
        self.assertRaises(scenario_base.NoOperation,
                          self.scenario.run, self.mock_user)
        self.mock_api.services.list.assert_called_once_with()

    @mock.patch('innervate.scenarios.create.CreateService._select_random_image')
    @mock.patch('innervate.scenarios.base.select_random_project')
    @mock.patch('innervate.scenarios.base.random_name')
    def test_run(self, mock_name, mock_select_proj, mock_select_image):
        # Setup
        mock_select_image.return_value = {
            'name': 'image1',
            'ports': '3000:TCP',
        }
        mock_select_proj.return_value = 'proj1'
        mock_name.return_value = 'service1'

        # Test
        report = self.scenario.run(self.mock_user)

        # Verify
        self.assertTrue(isinstance(report, scenario_base.ScenarioRunReport))
        self.assertEqual('proj1', report.project_name)
        self.assertEqual('inn-service1', report.service_name)

        self.mock_api.services.list.assert_called_once_with()
        self.mock_api.services.create_from_image.assert_called_once_with(
            'inn-service1', 'image1', project_name='proj1',
            ports=[(3000, 'TCP')])

