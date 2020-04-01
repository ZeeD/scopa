#!/usr/bin/env python

import setuptools

setuptools.setup(name='scopa',
                 version='0.0.1',
                 description='Scopa',
                 package_dir={
                     '': 'src'
                 },
                 packages=setuptools.find_packages(where='src'),
                 python_requires='>=3',
                 package_data={
                     'sample': [
                         'data/*'
                     ],
                 },
                 entry_points={  # Optional
                     'console_scripts': [
                         'bin/scopa',
                     ],
                 })
