from os import path


class VersionManage:
    def __init__(self, version_path='./script/__version__.md', step=32):
        self.step = step
        self.version_path = version_path
        self.version_arr = [0, 0, 1]
        self.read()

    @property
    def version(self):
        return '.'.join([str(i) for i in self.version_arr])

    def add(self):
        step = self.step
        version = self.version_arr
        version2 = version[0] * step * step + version[1] * step + version[2] + 1
        version[2] = version2 % step
        version[1] = int(version2 / step) % step
        version[0] = int(version2 / step / step)

        self.version_arr = version

    def read(self):
        if path.exists(self.version_path):
            with open(self.version_path, 'r') as f:
                self.version_arr = [int(i) for i in f.read().split('.')]
        else:
            self.version_arr = [0, 0, 1]

    def write(self):
        with open(self.version_path, 'w') as f:
            f.write(self.version)
        return self.version


def get_version(argv, version_path, step=10):
    manage = VersionManage(version_path, step=step)
    manage.read()
    if len(argv) >= 2 and argv[1] == 'build':
        manage.add()
        manage.write()
    return manage.version


def read_version(version_path):
    manage = VersionManage(version_path)
    manage.read()
    return manage.version
