# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import abc


class Scenario(object):

    def __init__(self, name, config):
        self.name = name
        self.config = config

    def __str__(self):
        return '[%s] %s' % (self.__class__.__name__, self.name)

    @abc.abstractmethod
    def run(self, user):
        pass
