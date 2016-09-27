# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import json

from innervate.api import OpenShiftAPI

USER_PREFIX = 'load_'


class UserManager(object):

    def __init__(self, admin_api, username_prefix=USER_PREFIX):
        super(UserManager, self).__init__()

        self.admin_api = admin_api
        self.username_prefix = username_prefix

    def create_users(self, count):
        for i in range(0, count):
            username = self.username_prefix + str(i)
            self.admin_api.create_user(username)
            self.admin_api.create_oauth_token(username)

    def delete_users(self):
        matching_users = self.get_usernames()
        for username in matching_users:
            self.admin_api.delete_oauth_token(username)
            self.admin_api.delete_user(username)

    def clean_oauth_tokens(self):
        response = self.admin_api.get_oauth_tokens()
        token_data = json.loads(response.text)

        for t in token_data['items']:
            if t['userName'].startswith(self.username_prefix):
                self.admin_api.delete_oauth_token(t['metadata']['name'])

    def get_usernames(self):
        response = self.admin_api.get_users()
        user_data = json.loads(response.text)

        users = [i['metadata']['name'] for i in user_data['items']]
        users = filter(lambda x: x.startswith(self.username_prefix), users)
        return users

    def get_user_tokens(self):
        response = self.admin_api.get_oauth_tokens()
        user_data = json.loads(response.text)

        users = {}
        for t in user_data['items']:
            username = t['userName']

            if not username.startswith(self.username_prefix):
                continue

            token = t['metadata']['uid']
            created = t['metadata']['creationTimestamp']

            u = users.get(username, None)
            if u is None:
                u = User(username)
                users[username] = u

            if created > u.token_creation_time:
                u.token = token
                u.token_creation_time = created

        user_tokens = {u.username: u.token for u in users.values()}
        return user_tokens

    def get_user_projects(self):
        user_tokens = self.get_user_tokens()

        for username, token in user_tokens.items():
            print('User: %s, Token: %s' % (username, token))
            user_api = OpenShiftAPI(self.admin_api.host, username)
            user_api.token = token

            print('Projects for %s' % username)
            print(user_api.get_projects())

class User(object):

    def __init__(self, username):
        super(User, self).__init__()
        self.username = username
        self.token = None
        self.token_creation_time = None
