"""
This ConfigManager and the user-facing configuration functionality.
"""

from configparser import ConfigParser

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController


class ConfigManager(AbstractBaseController):
  """The Config Manager handles the application persisted configuration in ~/.pvmanager/config."""
  class Meta:
    """The Config Manager meta configuration."""
    label = 'config'
    description = """
      Config manager handles the persisted configuration settings.
      Config file is located at ~/.pvmanager/config.
      """
    arguments = [
        (['extra_arguments'], dict(action='store', nargs='*'))
    ]

  def __init__(self):
    AbstractBaseController.__init__(self)
    self.config_path = self.home_path / 'config'

  def _setup(self, app_obj):
    """The config controller setup."""
    super(ConfigManager, self)._setup(app_obj)

    if not self.config_path.exists():
      app_obj.log.info('creating config file ({})'.format(self.config_path))
      self.config_path.touch()

  def _validate_extra_arguments(self, count):
    size = len(self.app.pargs.extra_arguments)
    if 0 == size or count < size:
      self.app.log.error('expected only one property')
      return False
    return True

  def _render(self, result):
    print('  {}'.format(result))

  @expose(hide=True)
  def default(self):
    """Default command handler just prints out the help information."""
    self.app.args.print_help()

  @expose(help='Prints a config property')
  def get(self):
    """The `get` command prints out the desired config property."""
    if self._validate_extra_arguments(1):
      prop = self.app.pargs.extra_arguments[0]
      self._render('{prop_name} = "{prop_value}"'.format(prop_name=prop, prop_value=self.get_config(prop)))

  @expose(help='Saves a config property')
  def set(self):
    """The `set` command saves the desired config property to the config file."""
    if self._validate_extra_arguments(2):
      prop_name = self.app.pargs.extra_arguments[0]
      prop_value = self.app.pargs.extra_arguments[1]

      config = ConfigParser()
      config.read(self.config_path)

      if not config.sections():
        config.add_section(self.app_name)

      config[self.app_name][prop_name] = prop_value

      with open(self.config_path, 'w') as config_file:
        config.write(config_file)
        self.app.log.info('new prefix saved')
