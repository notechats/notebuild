import os

from notebuild.shell import run_shell


class ServerManage:
    def __init__(self):
        self.manage_conf_path = "/notechats/notebuild/supervisord.conf"
        self.conf_dir = "/notechats/notebuild/conf"

    def init(self):
        run_shell(f"mkdir -p {self.conf_dir}")
        run_shell(f"cp -f {os.path.abspath(os.path.dirname(__file__))}/supervisord.conf {self.manage_conf_path}")

    def init2(self):
        run_shell(f"mkdir -p {self.conf_dir}")
        run_shell(f"echo_supervisord_conf > {self.manage_conf_path}")
        append_data = f"""
[include]
files = {self.conf_dir}/*.ini
        """
        data = open(self.manage_conf_path, 'r').read()
        data += append_data
        with open(self.manage_conf_path, 'w') as f:
            f.write(data)

    def start(self):
        cmd = f"supervisord -c {self.manage_conf_path}"
        print(cmd)
        run_shell(cmd)

    def add_job(self, server_name, directory, command, user='bingtao', stdout_logfile=None):
        default_logfile = f'/notechats/logs/notebuild/{server_name}.log'
        config = f"""[program:{server_name}]
directory = {directory}
command = {command} 
autostart = true
autorestart = true
user = {user}
stdout_logfile = {stdout_logfile or default_logfile}
        """
        with open(f'{self.conf_dir}/{server_name}.ini', 'w') as f:
            f.write(config)


class BaseServer:
    def __init__(self, server_name='base_server', current_path=None, *args, **kwargs):
        self.server_name = server_name
        self.current_path = current_path or os.path.abspath(os.path.dirname(__file__))
        self.manage = ServerManage()

    def init(self):
        pass

    def status(self):
        run_shell(f"supervisorctl -c {self.manage.manage_conf_path} status")

    def stop(self):
        run_shell(f"supervisorctl -c {self.manage.manage_conf_path} stop {self.server_name}")

    def start(self):
        run_shell(f"supervisorctl -c {self.manage.manage_conf_path} start {self.server_name}")

    def restart(self):
        run_shell(f"supervisorctl -c {self.manage.manage_conf_path} restart {self.server_name}")
