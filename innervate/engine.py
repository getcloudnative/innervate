# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from innervate.api import OpenShiftAPI
from innervate.user import UserManager


class InnervateEngine(object):
    """Driving engine for running the simulations."""

    def __init__(self, config):
        super(InnervateEngine, self).__init__()

        self.user_manager = None
        self.config = config

    def initialize(self):

        # Create the manager responsible for tracking and authenticating users
        self.user_manager = UserManager(self.config.host,
                                        self.config.port)

        # Load each configured user
        for u in self.config.users:
            self.user_manager.load_user(u[0], u[1])

