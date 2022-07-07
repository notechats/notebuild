from notebuild.core.version import VersionManage


def read_version(version_path):
    manage = VersionManage(version_path)
    manage.read()
    return manage.version
