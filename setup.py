from setuptools import setup, find_packages

name = 'upstart-shield'
version = '0.1'

setup(
    name=name, version=version,
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'upstart-shield=upstart_shield.scripts:main',
            'upstart-shield-test-master='
            'upstart_shield.scripts:test_master_process',
            'upstart-shield-test='
            'upstart_shield.scripts:test_parent_process',
        ],
    },
)
