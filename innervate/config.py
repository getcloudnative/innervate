# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import logging.config
import os
import urllib2
import yaml

from pykube import KubeConfig


ENV_CONFIG = 'INNV_CONFIG'
ENV_HOST = 'INNV_HOST'


class InnervateConfig(object):

    def __init__(self):
        super(InnervateConfig, self).__init__()
        self._config = None

    def load(self, filename):
        with open(filename) as f:
            self._config = yaml.load(f)
        self._init_logging()

    def load_url(self, url):
        u = urllib2.urlopen(url)
        self._config = yaml.load(u.read())
        self._init_logging()

    def _init_logging(self):
        logging.config.dictConfig(self._config['logging'])

    @property
    def host(self):
        h = os.environ.get(ENV_HOST, None)
        if h:
            return h
        return self._config['host']

    @property
    def port(self):
        return self._config['port']

    @property
    def users(self):
        """Returns list of username/password tuples"""
        return [(u['username'], u['password']) for u in self._config['users']]

    @property
    def scenarios(self):
        return self._config['scenarios']

    @property
    def scenario_sleep_range(self):
        value = self._config['engine']['scenario_sleep_range']
        values = value.split('-')
        return int(values[0]), int(values[1])

    @property
    def log_state_every(self):
        value = self._config['engine'].get('log_state_every', None)
        if value:
            return int(value)
        else:
            return None

    @property
    def auto_clean(self):
        return self._config['engine'].get('auto_clean', False)

    def scenarios_for_type(self, type_name):
        x = [c for c in self.scenarios if c['type'] == type_name]
        return x


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
