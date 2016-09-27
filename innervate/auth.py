# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import requests
import requests.auth
import urlparse


AUTH_PATH = '/oauth/authorize?response_type=token&client_id=openshift-challenging-client'


def login(host, port, username, password):
    """Logs into an OpenShift server and returns the user's token."""

    headers = {'X-Csrf-Token': '1'}
    host = "https://{}:{}".format(host, port)
    url = urlparse.urljoin(host, AUTH_PATH)
    auth = requests.auth.HTTPBasicAuth(username, password)

    response = requests.get(url, verify=False, headers=headers, auth=auth)

    parsed_url = urlparse.urlparse(response.url)
    token_frags = parsed_url.fragment.split('&')
    token_pieces = {m.split('=')[0]: m.split('=')[1] for m in token_frags}
    token = token_pieces['access_token']

    return token
