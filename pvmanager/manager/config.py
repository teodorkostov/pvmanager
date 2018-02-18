from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController


class ConfigManager(AbstractBaseController):
  """The Config Manager handles the application persisted configuration in /home/$user/.$app_name/config."""
  class Meta:
    """The Media Manager meta configuration."""
    label = "config"
    description = """
      Config manager handles the persisted configuration settings.
      Config file is located at ~/.pvmanager/config.
      """
    arguments = [
        (['extra_arguments'], dict(action='store', nargs='*'))
    ]

  def _setup(self, app_obj):
    """The config controller setup."""
    super(ConfigManager, self)._setup(app_obj)

    config_path = self.home_path / "config"
    if not config_path.exists():
      app_obj.log.info("creating config file (%s)" % config_path)
      config_path.touch()

  @expose(hide=True)
  def default(self):
    """Default command handler just prints out the help information."""
    self.app.args.print_help()

  @expose(help="Prints a config property")
  def get(self):
    """The `get` command prints out the desired config property."""
    self.app.log.info(self.app.pargs)
