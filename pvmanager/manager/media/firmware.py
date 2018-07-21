"""
This FirmwareMediaManager all relevant functionality.
"""


from pvmanager.generic_media_controller import GenericMediaController



class FirmwareMediaManager(GenericMediaController):
  """The Firmware Media Manager handles the firmware media in $prefix/media/firmware/."""


  class Meta:
    """The Firmware Media Manager meta configuration."""
    label = 'firmware'
    description = """
    Firmware Media Manager handles the firmware media resources.
    All files are located at $prefix/media/firmware/.
    """
