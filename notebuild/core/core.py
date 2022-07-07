"""
打包的工具类
"""
import argparse
import logging
import os.path

from git import Repo
from notebuild.core.version import VersionManage
from notebuild.shell import run_shell, run_shell_list


class PackageBuild:
    """
    打包的工具类
    """

    def __init__(self, name=None):
        self.repo_path = run_shell("git rev-parse --show-toplevel", printf=False)
        self.name = name or self.repo_path.split('/')[-1]
        self.repo = Repo(self.repo_path)

        # self.git_url = run_shell("git remote -v", printf=False).split('\n')[0].split('\t')[1].split(' ')[0]
        self.git_url = [url for url in self.repo.remote().urls][0]
        self.version_manage = VersionManage(f'{self.repo_path}/script/__version__.md')

    def git_pull(self):
        """
        git pull
        """
        logging.info("{} pull".format(self.name))
        # run_shell("git pull")
        self.repo.remote().pull()

    def git_push(self):
        """
        git push
        """
        logging.info("{} push".format(self.name))
        run_shell_list([
            'git add -A',
            'git commit -a -m "add"',
            'git push'
        ])
        self.repo.index.add(f"{self.repo_path}/*")
        self.repo.index.commit(message='add')
        self.repo.remote().pull()

    def git_install(self):
        """
        git install
        """
        logging.info('{} install'.format(self.name))
        run_shell_list([
            'pip uninstall {} -y'.format(self.name),
            'python3 setup.py install',
            'rm -rf {}.egg-info'.format(self.name),
            'rm -rf dist',
            'rm -rf build'
        ])
        self.git_clear_build()

    def pip_install(self):
        """
        pip install
        """
        run_shell('pip install -U -q git+{}'.format(self.git_url))
        logging.info('pip install {} success'.format(self.name))

    def git_clear_build(self):
        logging.info('{} build clear'.format(self.name))
        run_shell_list([
            'rm -rf {}.egg-info'.format(self.name),
            'rm -rf dist',
            'rm -rf build',
        ])

    def git_build(self):
        """
        git build
        """
        logging.info('{} build'.format(self.name))
        self.git_pull()
        self.git_clear_build()
        self.version_manage.add()
        self.version_manage.write()
        set_up_file = 'setup.py'
        if not os.path.exists(set_up_file):
            set_up_file = 'setup2.py'
        if not os.path.exists(set_up_file):
            set_up_file = 'setup3.py'

        run_shell_list([
            f'python3 {set_up_file} build',  # 编译
            f'python3 {set_up_file} sdist',  # 生成 tar.gz
            f'python3 {set_up_file} bdist_egg',  # 生成 egg 包
            f'python3 {set_up_file} bdist_wheel',  # 生成 wheel 包

            # twine register dist/*
            'twine upload dist/*'  # 发布包
        ])
        self.git_clear_build()
        self.git_push()
        self.git_tags()
        self.pip_install()

    def git_clean_history(self):
        """
        git build
        """
        logging.info(f'{self.name} clean history')
        run_shell_list([
            'git tag -d $(git tag -l) || true',         # 删除本地 tag
            'git fetch',                                # 拉取远程tag
            'git push origin --delete $(git tag -l)',   # 删除远程tag
            "git tag -d $(git tag -l) || true",         # 删除本地tag
            'git checkout --orphan latest_branch',      # 1.Checkout
            'git add -A',                               # 2.Add all the files
            'git commit -am "clear history"',           # 3.Commit the changes
            'git branch -D master',                     # 4.Delete the branch
            'git branch -m master',                     # 5.Rename the current branch to master
            'git push -f origin master',                # 6.Finally, force update your repository
            'git push --set-upstream origin master',
            f'echo {self.name} success'
        ])

    def git_clean(self):
        """
        git clean
        """
        logging.info('{} clean'.format(self.name))
        run_shell_list([
            'git rm -r --cached .',
            'git add .',
            "git commit -m 'update .gitignore'",
            'git gc --aggressive',
        ])

    def git_tags(self):
        self.repo.create_tag(f'v{self.version_manage.version}')
        self.repo.remote().push()
        self.repo.remote().push(self.repo.tags)

    def git_tags_clear(self):
        for tag in self.repo.tags:
            self.repo.delete_tag(tag)
        self.repo.remote().push()
        self.repo.remote().push(self.repo.tags)


def command_line_parser():
    parser = argparse.ArgumentParser(description="Test")
    parser.add_argument('command')
    args = parser.parse_args()
    return args


def notebuild():
    """
    build tool
    """
    args = command_line_parser()
    package = PackageBuild()
    if args.command == 'pull':
        package.git_pull()
    elif args.command == 'push':
        package.git_push()
    elif args.command == 'install':
        package.git_install()
    elif args.command == 'build':
        package.git_build()
    elif args.command == 'clean':
        package.git_clean()
    elif args.command == 'clean_history':
        package.git_clean_history()
    elif args.command == 'tags':
        package.git_tags()
    elif args.command == 'help':
        info = """
build 
pull
push
install
clean
clean_history
help
tags
        """
        print(info)
