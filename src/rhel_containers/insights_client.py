INSIGHTS_CLIENT_CONF = """[insights-client]
base_url= {base_url}
cert_verify=False
auto_config=False
legacy_upload=False
authmethod=CERT"""


class InsightsClient:
    def __init__(self, engine, config, env="qa"):
        self.engine = engine
        self.config = config
        self.env = env

    def install(self, pkg="insights-client"):
        """Install insights-client packges

        Args:
            pkg: insights-client package with specific version.
        """
        self.engine.install_pkg(pkg)

    def configure(self):
        if self.env == "prod":
            print("For prod env no need of config.")
            return
        conf = INSIGHTS_CLIENT_CONF.format(base_url=self.config.insights_client.entrypoint)
        return self.engine.add_file(self.config.insights_client.conf_path, content=conf)

    def register(self, disable_schedule=None, keep_archive=None, no_upload=None):
        cmd = "insights-client --register"
        if disable_schedule:
            cmd = f"{cmd} --disable-schedule"
        if keep_archive:
            cmd = f"{cmd} --keep-archive"
        if no_upload:
            cmd = f"{cmd} --no-upload"

        # In rhel container sometime hostname pkg missing and insights-client need this package.
        if not self.engine.is_pkg_installed("hostname"):
            self.engine.install_pkg("hostname")

        # If insights-client not installed then installed it first.
        if not self.engine.is_pkg_installed("insights-client"):
            self.install()

        return self.engine.exec(cmd)

    def unregister(self):
        return self.engine.exec("insights-client --unregister")

    @property
    def version(self):
        return self.engine.exec("insights-client --version")