"""
This VmManager and the VM configuration functionality.
"""

from pathlib import Path

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController


class VmManager(AbstractBaseController):
  """The VM Manager handles the VM configurations in $prefix/vm/."""
  class Meta:
    """The VM Manager meta configuration."""
    label = 'vm'
    description = """
      VM manager handles the VM configurations.
      All VM config files are located at $prefix/vm/.
      """
    arguments = [
        (['extra_arguments'], dict(action='store', nargs='*'))
    ]

  def __init__(self):
    AbstractBaseController.__init__(self)
    self.vm_path = None

  def _setup(self, app_obj):
    """The VM controller setup."""
    super(VmManager, self)._setup(app_obj)

    self.vm_path = Path(self.get_config('prefix')) / 'vm'

    if not self.vm_path.exists():
      app_obj.log.info('creating VM path ({})'.format(self.vm_path))
      self.vm_path.mkdir()

  def _render(self, result):
    print('  {}'.format(result))

  @expose(hide=True)
  def default(self):
    """Default command handler just prints out the help information."""
    self.app.args.print_help()

  @expose(help='List all VM configurations in the current PREFIX.')
  def list(self):
    self.app.render(dict(data=self.vm_path.iterdir()), "list.m")
