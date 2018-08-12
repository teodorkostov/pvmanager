"""
This VmManager and the VM configuration functionality.
"""

from pathlib import Path
import yaml

from cement.core.controller import expose
from humanfriendly import parse_size

from pvmanager.abstract_base_controller import AbstractBaseController



CREATE_USAGE = 'usage: ... vm create <VM name> [<installation media file path> ...]'
RUN_USAGE = 'usage: ... vm run <VM name> [<mode>]'

INSTALL_MEDIA_KEY = 'install_media'
MEMORY_KEY = 'memory'
NETWORK_INTERFACE_KEY = 'network_interface'
SOUND_KEY = 'sound'

class VmManager(AbstractBaseController):
  """The VM Manager handles the VM configurations in $prefix/vm/."""

  class Meta:
    """The VM Manager meta configuration."""
    label = 'vm'
    description = """
    VM manager handles the VM configurations.
    All VM config files are located at $prefix/vm/.
    """
    config_defaults = dict(
      memory='3G',
      network_interface='tap0'
    )
    arguments = [
      (['-m', '--memory'], dict(action='store', help='[K, KB, KiB, M, G, ...] VM memory size ({})'.format(config_defaults[MEMORY_KEY]))),
      (['-n', '--network-interface'], dict(action='store', help='network interface name ({})'.format(config_defaults[NETWORK_INTERFACE_KEY]))),
      (['-s', '--sound'], dict(action='store', help='[pa, alsa] sound configuration')),
      (['extra_arguments'], dict(action='store', nargs='*'))
    ]


  def __init__(self):
    AbstractBaseController.__init__(self)
    self.vm_path = None


  def _setup(self, app_obj):
    """The VM controller setup."""
    super(VmManager, self)._setup(app_obj)

    self.vm_path = Path(self.get_config('prefix')) / self.Meta.label

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
    if 1 > size:
      self.app.log.error(CREATE_USAGE)
      return

    vm_instance_path = self._get_vm_path(self.app.pargs.extra_arguments[0].safe_value)

    # prepare the general template
    template_arguments = {
      'original_name': self.app.pargs.extra_arguments[0].original_value,
      'safe_name': vm_instance_path.stem,
      MEMORY_KEY: parse_size(self.get_config(MEMORY_KEY), binary=True),
      NETWORK_INTERFACE_KEY: self.get_config(NETWORK_INTERFACE_KEY),
      INSTALL_MEDIA_KEY: []
    }

    # prepare the installation media
    media_index = 0
    for argument in self.app.pargs.extra_arguments[1::]:
      template_arguments[INSTALL_MEDIA_KEY].append(dict(media_path=argument, media_index=media_index))
      media_index += 1

    template_arguments['has_{}'.format(INSTALL_MEDIA_KEY)] = 0 < len(template_arguments[INSTALL_MEDIA_KEY])

    # prepare the sound config
    sound_driver = self.app.pargs.sound
    if 'pa' == sound_driver:
      template_arguments[SOUND_KEY] = [
        {'key': 'QEMU_AUDIO_DRV', 'value': 'pa'}
      ]
    elif 'alsa' == sound_driver:
      template_arguments[SOUND_KEY] = [
        {'key': 'QEMU_AUDIO_DAC_FIXED_FREQ', 'value': 192000},
        {'key': 'QEMU_AUDIO_DAC_FIXED_FMT', 'value': 'S32'},
        {'key': 'QEMU_AUDIO_DRV', 'value': 'alsa'},
        {'key': 'QEMU_ALSA_DAC_DEV', 'value': 'default'},
        {'key': 'QEMU_ALSA_DAC_PERIOD_SIZE', 'value': 512},
        {'key': 'QEMU_ALSA_DAC_BUFFER_SIZE', 'value': 8192},
        {'key': 'QEMU_ALSA_ADC_DEV', 'value': 'null'}
      ]

    template_arguments['has_{}'.format(SOUND_KEY)] = None != sound_driver

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
      vm_instance = yaml.load(stream)

      vm_run_mode = self.app.pargs.extra_arguments[1].original_value if 1 < len(self.app.pargs.extra_arguments) else 'default'
      run_options = vm_instance['qemu']['run'][vm_run_mode]

      self.app.log.info('running configuration: {}'.format(vm_run_mode))
      self.app.log.info('components: {}'.format(run_options))

      qemu_options = {}
      for run_option in run_options:
        config_option = vm_instance['qemu']['config'][run_option]
        qemu_options = {**qemu_options, **config_option}

      self.app.log.debug('QEMU options: {}'.format(qemu_options))

      qemu_arguments = []
      for option, payload in qemu_options.items():
        if isinstance(payload, list):
          for value in payload:
            qemu_arguments.append('-{}'.format(option))
            qemu_arguments.append(value)
        else:
          qemu_arguments.append('-{}'.format(option))
          qemu_arguments.append(payload)

      self.app.log.debug('QEMU arguments: {}'.format(qemu_arguments))

      print(qemu_arguments)
