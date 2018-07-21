"""
This ImageMediaManager all relevant functionality.
"""

import subprocess

from cement.core.controller import expose

from pvmanager.generic_media_controller import GenericMediaController



class ImageMediaManager(GenericMediaController):
  """The Image Media Manager handles the VM media in $prefix/media/image/."""


  class Meta:
    """The Image Media Manager meta configuration."""
    label = 'image'
    description = """
    Image Media Manager handles the VM media resources (images).
    All files are located at $prefix/media/image/.
    """


  def _get_image_path(self, general_vm_name):
    return self.media_path / '{}.raw'.format(general_vm_name)


  @expose(help='Create a new VM image in the current PREFIX.')
  def create(self):
    """Handler for the image creation."""
    size = len(self.app.pargs.extra_arguments)
    if 2 > size:
      self.app.log.error('usage: ... image create <VM name> <size>')
      return

    general_vm_name = self.app.pargs.extra_arguments[0]
    vm_image_path = self._get_image_path(general_vm_name)
    vm_image_size = self.app.pargs.extra_arguments[1]

    if vm_image_path.exists():
      self.app.log.error(
          'a VM image with the same name ({}) already exists'.format(vm_image_path.stem))
      return

    subprocess_arguments = ['qemu-img', 'create', '-f', 'raw', vm_image_path, vm_image_size]

    subprocess.call(subprocess_arguments)


  @expose(help='List all VM images in the current PREFIX.')
  def list(self):
    self.app.render(dict(data=self.media_path.iterdir()), "list.m")
