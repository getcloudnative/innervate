# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from innervate.objects import Project


class OpenShiftAPI(object):

    def list_project_names(self, user):
        projects_data = Project.objects(user.api)
        names = [p.name for p in projects_data]
        return names
