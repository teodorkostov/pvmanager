"""
This VmManager and the VM configuration functionality.
"""

from pathlib import Path
import yaml

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController



CREATE_USAGE = 'usage: ... vm create <VM name> <memory size in MB> <network interface name> [<installation media file path> ...]'
RUN_USAGE = 'usage: ... vm run <VM name> [<mode>]'

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

    vm_instance_path = self._get_vm_path(self.app.pargs.extra_arguments[0].safe_value)

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

    template_arguments['has_install_media'] = 0 < len(template_arguments['install_media'])

    self.app.render(template_arguments, 'app.yaml')


  @expose(help='Run a VM configuration from the current PREFIX.')
  def run(self):
    size = len(self.app.pargs.extra_arguments)
    if 1 > size:
      self.app.log.error('expected the VM name as an extra argument')
      return

    vm_instance_path = self._get_vm_path(self.app.pargs.extra_arguments[0].safe_value)

    if not vm_instance_path.exists():
      self.app.log.error('the selected VM ({}) does not exist'.format(vm_instance_path.stem))
      return

    self.app.log.info('running VM "{}"'.format(vm_instance_path.stem))

    with vm_instance_path.open() as stream:
      vm_run_mode = self.app.pargs.extra_arguments[1].original_value if 1 < len(self.app.pargs.extra_arguments) else 'default'
      vm_instance = list(yaml.load_all(stream))[1]
      self._render(vm_run_mode)
      self._render(vm_instance)

      base = vm_instance['qemu']['config']['base']
      install = vm_instance['qemu']['config']['install']
      self._render(base)
      self._render(install)
      qemu_options = {**base, **install}
      self._render(qemu_options)

      subprocess_arguments = []
      for option, payload in qemu_options.items():
        print('option {} is {}'.format(payload, type(payload)))
        if isinstance(payload, list):
          for value in payload:
            print(value)
            subprocess_arguments.append('-{}'.format(option))
            subprocess_arguments.append(value)
        else:
          subprocess_arguments.append('-{}'.format(option))
          subprocess_arguments.append(payload)

      print('>>> ready')
      print(subprocess_arguments)
