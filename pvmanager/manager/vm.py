"""
This VmManager and the VM configuration functionality.
"""

from pathlib import Path
import re
import yaml

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController


def convert_general_to_snake(general_name):
  no_spaces = re.sub('[\t \-*+]', '_', general_name)
  no_camel_case = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', no_spaces)
  extended_snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', no_camel_case).lower()
  snake_case = re.sub('_+', '_', extended_snake_case)
  return re.sub('^_|_$', '', snake_case)

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

  @expose(help='Create a new VM configuration in the current PREFIX.')
  def create(self):
    size = len(self.app.pargs.extra_arguments)
    if 1 > size:
      self.app.log.error('expected the VM name as an extra argument')
      return

    vm_name = self.app.pargs.extra_arguments[0]
    self._render(vm_name)
    safe_vm_name = convert_general_to_snake(vm_name)
    self._render(safe_vm_name)

  @expose(help='Run a VM configuration from the current PREFIX.')
  def run(self):
    size = len(self.app.pargs.extra_arguments)
    if 1 > size:
      self.app.log.error('expected the VM name as an extra argument')
      return

    vm_instance_path = self.vm_path / self.app.pargs.extra_arguments[0]
    self.app.log.info('running VM {}'.format(self.app.pargs.extra_arguments[0]))

    with vm_instance_path.open() as stream:
      vm_instance = yaml.load(stream)
      self._render(vm_instance)
