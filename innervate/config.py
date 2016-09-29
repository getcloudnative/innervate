# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import yaml

from pykube import KubeConfig


class InnervateConfig(object):

    def __init__(self):
        super(InnervateConfig, self).__init__()
        self._config = None

    def load(self, filename):
        with open(filename) as f:
            self._config = yaml.load(f)

    @property
    def host(self):
        return self._config['host']

    @property
    def port(self):
        return self._config['port']

    @property
    def users(self):
        """Returns list of username/password tuples"""
        return [(u['username'], u['password']) for u in self._config['users']]


class PykubeConfig(KubeConfig):

    def __init__(self, host, port, username, token):
        doc = {
            'apiVersion': 'v1',
            'kind': 'Config',
            "clusters": [
                {
                    "name": "self",
                    "cluster": {
                        "server": "https://{}:{}".format(host, port),
                        "insecure-skip-tls-verify": "true",
                    },
                },
            ],
            "users": [
                {
                    "name": username,
                    "user": {
                        "token": token,
                    },
                },
            ],
            "contexts": [
                {
                    "name": "self",
                    "context": {
                        "cluster": "self",
                        "user": username,
                        'namespace': 'test-1'
                    },
                }
            ],
            "current-context": "self",
        }

        super(PykubeConfig, self).__init__(doc)
