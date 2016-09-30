# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.


from . import base


class CreateService(base.Scenario):
    """Creates a new service.

    Configuration:
    * image_list: comma-separated list of image names to randomly choose from when
           creating the service
    * max_services_per_user: maximum number of services to deploy for each user; if
           this scenario is called and the number of services is at the max, no
           action will be taken
    """

    def run(self, user):
        if len(user.api.list_services()) >= self.config['max_services_per_user']:
            raise base.NoOperation('The user is already at the maximum service count of [%s]' %
                                   self.config['max_services_per_user'])
