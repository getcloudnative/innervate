#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from setuptools import setup, find_packages


setup(
        name='innervate',
        version='0.1.0',
        description='User and load simulator for OpenShift',
        license='GPLv2',

        author='Jay Dobies',
        author_email='jason.dobies@redhat.com',

        packages = find_packages(),

        test_suite = 'nose.collector',

        classifiers = [
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Programming Language :: Python'
        ],
)
