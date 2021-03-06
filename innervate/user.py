# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import logging
import pykube
import random

from .api import OpenShiftAPI
from .config import PykubeConfig
from . import auth


LOG = logging.getLogger(__name__)


class UserManager(object):

    def __init__(self, host, port):
        super(UserManager, self).__init__()

        # Used for token retrieval
        self.host = host
        self.port = port

        self.users = {}

    def load_user(self, username, password):
        """Mechanism for adding a user to the manager, loading the
        token and configuring the API in the process.

        :rtype: User
        """

        user = User(username)
        user.token = auth.login(self.host, self.port, username, password)
        user.config = PykubeConfig(self.host, self.port,
                                   user.username, user.token)
        user.http_client = pykube.HTTPClient(user.config)
        user.api = OpenShiftAPI(user.http_client)

        self.users[user.username] = user
        LOG.debug('Loaded user [%s]' % user.username)

    def user(self, username):
        return self.users[username]

    def random_user(self):
        return random.choice(self.users.values())

    @property
    def all_users(self):
        return self.users.values()

    def iterator(self):
        for u in self.users.values():
            yield u


class User(object):
    """Context information for a particular user."""

    def __init__(self, username):
        super(User, self).__init__()
        self.username = username

        # Static for the user itself
        self.config = None
        self.http_client = None
        self.api = None  # type: OpenShiftAPI
