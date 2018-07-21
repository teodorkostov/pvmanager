"""
This VmManager and the VM configuration functionality.
"""

from pathlib import Path
import yaml

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController



CREATE_USAGE = 'usage: ... vm create <VM name> <memory size in MB> <network interface name> [<installation media file path> ...]'

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


  def _get_vm_path(self, general_vm_name):
    return self.vm_path / '{}.yaml'.format(general_vm_name)


  @expose(help='List all VM configurations in the current PREFIX.')
  def list(self):
    self.app.render(dict(data=self.vm_path.iterdir()), "list.m")


  @expose(help="""
    Create a new VM configuration.
    {}
  """.strip().format(CREATE_USAGE))
  def create(self):
    size = len(self.app.pargs.extra_arguments)
    if 3 > size:
      self.app.log.error(CREATE_USAGE)
      return

    vm_name = self.app.pargs.extra_arguments[0].safe_value
    vm_instance_path = self._get_vm_path(vm_name)

    if vm_instance_path.exists():
      self.app.log.error('a VM with the same name ({}) already exists'.format(vm_instance_path.stem))
      return

    self._render(vm_instance_path)

    template_arguments = {
      'original_name': self.app.pargs.extra_arguments[0].original_value,
      'safe_name': vm_instance_path.stem,
      'memory_size_mb': self.app.pargs.extra_arguments[1].original_value,
      'net_ifname': self.app.pargs.extra_arguments[2].original_value,
      'install_media': []
    }

    media_index = 0
    for argument in self.app.pargs.extra_arguments[3::]:
      template_arguments['install_media'].append(dict(media_path=argument, media_index=media_index))
      media_index += 1

    self.app.render(template_arguments, 'app.yaml')


  @expose(help='Run a VM configuration from the current PREFIX.')
  def run(self):
    size = len(self.app.pargs.extra_arguments)
    if 1 > size:
      self.app.log.error('expected the VM name as an extra argument')
      return

    vm_instance_path = self._get_vm_path(self.app.pargs.extra_arguments[0])

    if not vm_instance_path.exists():
      self.app.log.error('the selected VM ({}) does not exist'.format(vm_instance_path.stem))
      return

    self.app.log.info('running VM "{}"'.format(vm_instance_path.stem))

    with vm_instance_path.open() as stream:
      vm_instance = yaml.load(stream)
      self._render(vm_instance)
