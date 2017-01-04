# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import base


class ConfigTests(base.BaseTestCase):

    def test_host(self):
        self.assertEqual('kubernetes', self.config.host)

    def test_port(self):
        self.assertEqual(8443, self.config.port)

    def test_users(self):
        # Count Test
        self.assertEqual(2, len(self.config.users))

        # Look for specific users with the format userX for name/pass
        for i in range(1, 3):
            u = 'user%s' % i
            self.assertTrue((u, u) in self.config.users)

    def test_scenarios(self):
        # There will be a lot of entropy in the example scenarios list,
        # and its on the scenarios themselves to validate the format, so
        # this test simply checks that we get a list of dicts that we
        # pass to each scenario and that they basic required components
        # are included
        self.assertTrue(isinstance(self.config.scenarios, list))
        for i in self.config.scenarios:
            self.assertTrue(isinstance(i, dict))
            self.assertTrue('name' in i)
            self.assertTrue('type' in i)
            # I can probably assume config is required, but I'm ok not
            # testing for that for now




