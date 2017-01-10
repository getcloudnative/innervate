# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import time

import base


class DeleteProjectTests(base.BaseFunctionalTestCase):

    def test_delete(self):
        # Setup
        create_s = self.scenario('create-project')
        create_s.run(self.user)
        time.sleep(3)
        self.assert_projects_count(1)

        # Test
        delete_s = self.scenario('delete-project')
        delete_s.run(self.user)
        time.sleep(3)

        # Verify
        self.assert_no_projects()


class DeleteServicesTests(base.BaseFunctionalTestCase):

    def test_delete(self):
        # Setup
        create_p = self.scenario('create-project')
        create_p.run(self.user)
        time.sleep(3)
        project = self.user.api.projects.list().get()

        create_s = self.scenario('create-service')
        create_s.run(self.user)
        time.sleep(3)

        # Sanity Check
        all_services = self.user.api.services.list(project_name=project.name)
        self.assertEqual(1, len(all_services))

        # Test
        delete_s = self.scenario('delete-service')
        delete_s.run(self.user)
        time.sleep(3)

        # Verify
        project = self.user.api.projects.list().get()
        all_services = self.user.api.services.list(project_name=project.name)
        self.assertEqual(0, len(all_services))
