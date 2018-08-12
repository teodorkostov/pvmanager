"""
This VmManager and the VM configuration functionality.
"""

from pathlib import Path
import subprocess
import yaml

from cement.core.controller import expose
from humanfriendly import parse_size

from pvmanager.abstract_base_controller import AbstractBaseController



CREATE_USAGE = 'usage: ... <VM name> [<installation media file path> ...]'
RUN_USAGE = 'usage: ... <VM name> [<mode>]'

INSTALL_MEDIA_KEY = 'install_media'
MEMORY_KEY = 'memory'
NETWORK_INTERFACE_KEY = 'network_interface'
AUDIO_KEY = 'audio'



class VmBaseManager(AbstractBaseController):
  """The VM Base Manager sets up the default functionality needed by a VM manager"""


  def __init__(self):
    AbstractBaseController.__init__(self)
    self.vm_path = None


  def _setup(self, app_obj):
    """The VM controller setup."""
    super(VmBaseManager, self)._setup(app_obj)

    self.vm_path = Path(self.get_config('prefix')) / 'vm'

    if not self.vm_path.exists():
      app_obj.log.info('creating VM path ({})'.format(self.vm_path))
      self.vm_path.mkdir()


  def _get_vm_path(self, general_vm_name):
    return self.vm_path / '{}.yaml'.format(general_vm_name)



class VmManager(VmBaseManager):
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


  @expose(help='List all VM configurations in the current PREFIX.')
  def list(self):
    self.app.render(dict(data=self.vm_path.iterdir()), "list.m")


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
      vm_instance = yaml.load(stream)

      vm_run_mode = self.app.pargs.extra_arguments[1].original_value if 1 < len(self.app.pargs.extra_arguments) else 'default'
      run_options = vm_instance['qemu']['run'][vm_run_mode]

      self.app.log.info('running configuration: {}'.format(vm_run_mode))
      self.app.log.info('components: {}'.format(run_options))

      # prepare dict of run configurations
      qemu_options = {}
      for run_option in run_options:
        config_option = vm_instance['qemu']['config'][run_option]
        for key, value in config_option.items():
          if key in qemu_options:
            qemu_options[key] += value
          else:
            qemu_options[key] = value

      self.app.log.debug('QEMU options: {}'.format(qemu_options))

      # prepare the qemu arguments
      qemu_arguments = ['taskset', '-c', '1-3', 'qemu-system-x86_64']
      memory_option = None
      for option, payload in qemu_options.items():
        if 'm' == option:
          memory_option = payload
        if isinstance(payload, list):
          for value in payload:
            qemu_arguments.append('-{}'.format(option))
            qemu_arguments.append(value)
        else:
          qemu_arguments.append('-{}'.format(option))
          qemu_arguments.append(payload)

      self.app.log.debug('memory option: {}'.format(memory_option))
      self.app.log.debug('QEMU arguments: {}'.format(qemu_arguments))

      # prepare the audio options
      audio_arguments = vm_instance['qemu']['config'].get(AUDIO_KEY)

      self.app.log.debug('audio arguments: {}'.format(audio_arguments))

      # preparing the memory limits
      memory_size = parse_size(memory_option, binary=True)
      memory_argument = int(memory_size / 1024) + 1024

      print(memory_option)
      print(memory_size)
      print(memory_argument)
      print(audio_arguments)
      print(qemu_arguments)



class VmCreateManager(VmBaseManager):
  """The VM Create Manager provides the context for the create command."""
  class Meta:
    """The VM Create Manager meta configuration."""
    description = """
    Create a new VM configuration.
    {}
    """.strip().format(CREATE_USAGE)
    stacked_on = 'vm'
    label = 'vm_create'
    aliases = ['create']
    aliases_only = True
    config_defaults = dict(
        memory='3G',
        network_interface='tap0'
    )
    arguments = [
        (['-a', '--audio'], dict(action='store', help='[pa, alsa] audio configuration')),
        (['-m', '--memory'], dict(action='store', help='[K, KB, KiB, M, G, ...] VM memory size ({})'.format(config_defaults[MEMORY_KEY]))),
        (['-n', '--network-interface'], dict(action='store', help='network interface name ({})'.format(config_defaults[NETWORK_INTERFACE_KEY]))),
        (['extra_arguments'], dict(action='store', nargs='*'))
    ]

  @expose(hide=True)
  def default(self):
    """Default command handler just prints out the help information."""
    size = len(self.app.pargs.extra_arguments)
    if 1 > size:
      self.app.args.print_help()
      return

    vm_instance_path = self._get_vm_path(self.app.pargs.extra_arguments[0].safe_value)

    if vm_instance_path.exists():
      self.app.log.error('the selected VM ({}) already exists'.format(vm_instance_path.stem))
      return

    subprocess_arguments = ['pvmanager', 'vm', 'create', 'render']

    for argument, value in self.app.pargs.__dict__.items():
      if 'debug' == argument:
        continue
      if 'suppress_output' == argument:
        continue
      if 'extra_arguments' == argument:
        continue
      if value is not None:
        subprocess_arguments.append('--{}={}'.format(argument, value))

    subprocess_arguments.extend(map(str, self.app.pargs.extra_arguments))

    self.app.log.debug('render arguments: {}'.format(subprocess_arguments))

    with vm_instance_path.open('w') as stream:
      subprocess.call(subprocess_arguments, stdout=stream)

    self.app.log.info('successfully created new VM {}'.format(vm_instance_path.stem))


  @expose(hide=True)
  def render(self):
    """Default command handler just prints out the help information."""
    size = len(self.app.pargs.extra_arguments)
    if 1 > size:
      self.app.args.print_help()
      return

    vm_instance_path = self._get_vm_path(self.app.pargs.extra_arguments[0].safe_value)

    # prepare the general template
    template_arguments = {
      'original_name': self.app.pargs.extra_arguments[0].original_value,
      'safe_name': vm_instance_path.stem,
      MEMORY_KEY: self.get_config(MEMORY_KEY),
      NETWORK_INTERFACE_KEY: self.get_config(NETWORK_INTERFACE_KEY),
      INSTALL_MEDIA_KEY: []
    }

    # prepare the installation media
    media_index = 0
    for argument in self.app.pargs.extra_arguments[1::]:
      template_arguments[INSTALL_MEDIA_KEY].append(dict(media_path=argument, media_index=media_index))
      media_index += 1

    template_arguments['has_{}'.format(INSTALL_MEDIA_KEY)] = 0 < len(template_arguments[INSTALL_MEDIA_KEY])

    # prepare the audio config
    audio_driver = self.app.pargs.audio
    if 'pa' == audio_driver:
      template_arguments[AUDIO_KEY] = [
        {'key': 'QEMU_AUDIO_DRV', 'value': 'pa'}
      ]
    elif 'alsa' == audio_driver:
      template_arguments[AUDIO_KEY] = [
        {'key': 'QEMU_AUDIO_DAC_FIXED_FREQ', 'value': 192000},
        {'key': 'QEMU_AUDIO_DAC_FIXED_FMT', 'value': 'S32'},
        {'key': 'QEMU_AUDIO_DRV', 'value': 'alsa'},
        {'key': 'QEMU_ALSA_DAC_DEV', 'value': 'default'},
        {'key': 'QEMU_ALSA_DAC_PERIOD_SIZE', 'value': 512},
        {'key': 'QEMU_ALSA_DAC_BUFFER_SIZE', 'value': 8192},
        {'key': 'QEMU_ALSA_ADC_DEV', 'value': 'null'}
      ]

    template_arguments['has_{}'.format(AUDIO_KEY)] = None != audio_driver

    self.app.render(template_arguments, 'app.yaml')
