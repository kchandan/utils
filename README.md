utils
========

Small utilities for FreeIPA.

The user_import.py reads input from user.list file and push that into FreeIPA. This utility is helpful if you want to import shadow users into FreeIPA.

Usage:

Change the IPA hostname in the script
Keep the passwd and shadow file in the same directory that of user_import.py and make sure the users are in same order in both file.
execute it ./user_import.py

If you want something missing/bug please feel free to log an issue or send patch request.


sync_vm.sh

This script could be used to nightly synchronize the virtual machine images (KVM/qemu) with Virsh front end across multiple Physical boxes
It won't be highly available, however, it will provide a automated backup. Simple rsync script with some error handling.
