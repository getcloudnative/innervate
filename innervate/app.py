# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from optparse import OptionParser
import os
import sys
import urlparse

from innervate.config import (ENV_CONFIG, InnervateConfig)
from innervate.engine import InnervateEngine


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    options = parse_args(args)

    config = InnervateConfig()

    config_url = os.environ.get(ENV_CONFIG, None)
    if not config_url:
        ex = os.path.join(os.path.abspath('config'), 'example.yaml')
        config_url = urlparse.urljoin('file:', ex)
    config.load_url(config_url)

    engine = InnervateEngine(config)
    engine.initialize()

    if options.state:
        engine.log_current_state()
    elif options.clean:
        engine.cleanup()
    else:
        engine.run()


def parse_args(args):
    parser = OptionParser()
    parser.add_option('-s', '--state', dest='state', action='store_true',
                      help='Log the current state of each configured user\'s'
                           'account')
    parser.add_option('-l', '--clean', dest='clean', action='store_true',
                      help='Delete all projects for the configured users')
    options, args = parser.parse_args(args)
    return options


if __name__ == '__main__':
    main()
