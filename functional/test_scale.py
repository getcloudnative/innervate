# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import time

import base


class ScaleServiceTests(base.BaseFunctionalTestCase):

    def test_scale(self):
        # Setup
        create_p = self.scenario('create-project')
        create_p.run(self.user)
        time.sleep(3)

        create_s = self.scenario('create-service')
        create_s.run(self.user)
        time.sleep(3)

        # Test
        scale_s = self.scenario('scale-service-up')
        scale_s.run(self.user)
        time.sleep(3)
        scale_s.run(self.user)
        time.sleep(3)

        # Verify
        project = self.user.api.projects.list().get()
        service = self.user.api.services.list(project_name=project.name).get()
        replica_count = self.user.api.services.get_replica_count(service.name,
                                                                 project.name)
        self.assertEqual(3, replica_count)

