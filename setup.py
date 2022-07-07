import sys
from os import path

from setuptools import find_packages, setup


def get_version(argv, version_path, step=10):
    if path.exists(version_path):
        with open(version_path, 'r') as f:
            version1 = [int(i) for i in f.read().split('.')]
    else:
        version1 = [0, 0, 1]

    version3 = '{}.{}.{}'.format(*version1)
    with open(version_path, 'w') as f:
        f.write(version3)
    return version3


version_path = path.join(path.abspath(
    path.dirname(__file__)), 'script/__version__.md')

version = get_version(sys.argv, version_path, step=32)

install_requires = ['GitPython']

setup(name='notebuild',
      version=version,
      description='notebuild',
      author='niuliangtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',
      packages=find_packages(),
      package_data={"": ["*.js", "*.*"]},
      entry_points={'console_scripts': [
          'notebuild = notebuild.core:notebuild', ]},
      install_requires=install_requires,
      )
