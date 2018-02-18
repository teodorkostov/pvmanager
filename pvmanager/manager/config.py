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
      app_obj.log.info("creating config file ({})".format(config_path))
      config_path.touch()

  def _validate_extra_arguments(self):
    size = len(self.app.pargs.extra_arguments)
    if 0 == size or 1 < size:
      self.app.log.error("expected only one property")
      return False
    return True

  def _render(self, result):
    print("  {}".format(result))

  @expose(hide=True)
  def default(self):
    """Default command handler just prints out the help information."""
    self.app.args.print_help()

  @expose(help="Prints a config property")
  def get(self):
    """The `get` command prints out the desired config property."""
    if self._validate_extra_arguments():
      prop = self.app.pargs.extra_arguments[0]
      self._render("{prop_name} = '{prop_value}'".format(prop_name = prop, prop_value = self.get_config(prop)))
