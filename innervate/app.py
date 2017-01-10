# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import sys

from innervate.config import InnervateConfig
from innervate.engine import InnervateEngine


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    config = InnervateConfig()
    # TODO: Make a better reference to this
    config.load('config/example.yaml')

    engine = InnervateEngine(config)
    engine.initialize()
    engine.run()


if __name__ == '__main__':
    main()
