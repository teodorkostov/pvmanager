"""
This InstallMediaManager all relevant functionality.
"""


from pvmanager.generic_media_controller import GenericMediaController



class InstallMediaManager(GenericMediaController):
  """The Install Media Manager handles the install media in $prefix/media/install/."""


  class Meta:
    """The Install Media Manager meta configuration."""
    label = 'install'
    description = """
    Install Media Manager handles the install media resources.
    All files are located at $prefix/media/install/.
    """
