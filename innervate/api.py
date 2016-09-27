# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from innervate.objects import Project, ProjectRequest


class OpenShiftAPI(object):

    def __init__(self, user):
        super(OpenShiftAPI, self).__init__()
        self.user = user

    def list_project_names(self):
        projects_data = Project.objects(self.user.http_client)
        names = [p.name for p in projects_data]
        return names

    def create_project(self, project_name):
        p = ProjectRequest.new(self.user.http_client, project_name)
        p.create()

    def delete_project(self, project_name):
        p = Project.new(self.user.http_client, project_name)
        p.delete()
