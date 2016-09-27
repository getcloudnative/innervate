# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from innervate.api import OpenShiftAPI
from innervate.user import UserManager


class InnervateEngine(object):

    def __init__(self):
        super(InnervateEngine, self).__init__()

        self.user_manager = None
        self.openshift_api = None

    def initialize(self):

        # TODO: Eventually have these configurable
        host = 'kubernetes'
        port = '8443'

        self.user_manager = UserManager(host, port)

        # TODO: Temporary until loading user info from a file
        self.user_manager.load_user('user', 'user')

        self.openshift_api = OpenShiftAPI()
