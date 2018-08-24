# PVManager

Python VM Manager aims to provide a unified interface for managing VMs with the goal to extract the configuration aspects in a human readable format ([YAML](http://yaml.org/)).

In essense PVManager is a lightweight CLI wrapper for [QEMU](https://www.qemu.org/). However, with PCI or VGA passthrough, various images and tunning options the list of QEMU arguments becomes longer and longer. On top of that with every execution there are a number of additional commands that have to affect the QEMU process - like memory limits, prioritization and affinity. Running in a different mode (e.g. during installation or normal work) is quite annoying copy-pasting. Managing this with Bash scripts becomes hard especially when it has to be done for multiple VMs.

### Usage

NB: The project is super alpha so some manual tinkering is more than welcome.

NB: Knowledge of QEMU is needed.

```sh
# first it's a good idea to set the prefix - the location where the VM folder structure is created
$ pvmanager config set prefix /path/to/storage
# create a VM configuration (for more information on audio 'qemu-system-x86_64 -audio-help')
$ pvmanager vm create MyVM --audio alsa
# manually update the VM configuration according to your needs ;-)
# you can create an image yourself
$ pvmanager media image create MyVM 120G
# run your VM
$ pvmanager vm run MyVM
# PVManager tries to use safe names so the actual VM name is my_vm and can be used as well
$ pvmanager vm run my_vm
```
