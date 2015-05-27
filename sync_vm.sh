#!/bin/bash

# Puppet ready script
# This script will do
# 1. Suspend Local [remote] VM
# 2. Rsync the Image to local dir
# 3. Resume Local [remote] VM
# 4. Sync the image to remote

# Config Values
vm_name="<%= @profile_vmname %>"
vm_files="<%= @profile_vmfiles %>"
dest_ip="<%= @profile_destip %>"
hop_ip="<%= @profile_hopip %>"
user="<%= @profile_user %>"
dest_path="<%= @profile_destpath %>"
email_id="chandank@live.ca"
remote_check="<%= @profile_remotecheck %>"
enabled="<%= @profile_enabled %>"

virsh_bin=`which virsh`
rsync_bin="`which rsync` --partial -aqr"
ssh_bin="ssh -q $user@$dest_ip"
[[ -n "$hop_ip" ]] && ssh_bin="ssh -q $user@$hop_ip ssh -q $user@$dest_ip"
logger_bin="`which logger` sync_vm: "
to_dev_null="/dev/null 2>&1"
# Return Codes
return_ok=0
dont_pause=1
resume_failed=2
sync_failed=3
proc_abort=4

# Error and log Messages
emsg_resume="CRIT: Resume failed for VM :"
emsg_rsync="CRIT: Rsync Failed for VM :"
emsg_paused="CRIT: Pause Failed for VM :"

check_vmstate ()
{

    if [ $1 == "local" ]; then
        retval=`$sudo_cmd $virsh_bin list --all | grep "$vm_name" | awk '{print $3}'`
    elif [ $1 == "remote" ]; then
        retval=`$ssh_bin $virsh_bin list --all | grep "$vm_name" | awk '{print $3}'`
    fi

    if [ -z "$retval" ]; then
        $logger_bin "CRIT: $1 VM $vm_name does not exist";
        return $proc_abort
    elif [ $retval == "paused" ];then
        $logger_bin "CRIT: $1 VM $vm_name is already Paused Something is wrong!";
        return $dont_pause
    elif [ $retval == "shut" ]; then
        $logger_bin "CRIT: $1 VM $vm_name is Shutdown doing nothing"
        return $dont_pause
    elif [ $retval == "running" ]; then
        return $return_ok
    fi

}

pause_vm ()
{

    $sudo_cmd $virsh_bin suspend $vm_name > "$to_dev_null"
    if [ $? -ne 0 ];then
      $logger_bin $emsg_paused $vm_name "Exiting"
      exit 1
    fi

    if [ $remote_check == "yes" ]; then
        check_vmstate "remote"
        if [ $? -ne $return_ok ]; then
            return $?
        fi
        $ssh_bin $virsh_bin suspend $vm_name > "$to_dev_null"
    fi

}

sync_image_stage1 ()
{

    $rsync_bin $vm_files $HOME
    if [ $? -ne 0 ]; then
        $logger_bin "CRIT: Rsync stage1 Failed for $vm_name"
        return $sync_failed
    else
        return $return_ok
    fi

}

sync_image_stage2 ()
{

    $rsync_bin -e "$ssh_bin" $HOME/ :$dest_path
    if [ $? -ne 0 ]; then
        $logger_bin "CRIT: Rsync stage2 Failed for $vm_name"
        return $sync_failed
    else
        return $return_ok
    fi

}


resume_vm()
{

    $sudo_cmd $virsh_bin resume $vm_name > "$to_dev_null"
    if [ $? -ne 0 ]; then
        echo "$emsg_resume $vm_name." | mail -s "$emsg_resume $vm_name" $email_id
        $logger_bin $emsg_resume $vm_name
        return $resume_failed
    fi

    if [ $remote_check == "yes" ]; then
        check_vmstate "remote"
        if [ $? -ne $return_ok ]; then
            return $?
        fi
        $ssh_bin $virsh_bin resume $vm_name > "$to_dev_null"
    fi

}

#
# Start Of Execution
#

# Exit if not enabled
[[ $enabled != "yes" ]] && exit 0

# Use sudo if not root
if [ $user != 'root' ]; then
  to_dev_null='null_file'
  sudo_cmd='sudo '
fi

check_vmstate "local"
retval=$?
if [ $retval -eq $proc_abort ]; then
    $logger_bin "Nothing to do Exiting"
    exit 1
else
    pause_vm
fi

# First copy locally
sync_image_stage1
retcode=$?
resume_vm

# Ensuring again that vm is running
check_vmstate "local"
retval=$?
if [ $retval -eq $return_ok ] && [ $retcode -eq $return_ok ]; then
    $logger_bin "VM sync stage1 done successfully!"
else
    resume_vm
fi

# Remote Rsync
sync_image_stage2
# If sync failed due to network try again
if [ $? == $sync_failed ]; then
  sync_image_stage2
else
  $logger_bin "VM sync stage2 done successfully!"
fi
