#!/usr/bin/python -tt
# This is a Free and Open Source Software

import sys
import os

passwd_file = 'passwd'
shadow_file = 'shadow'
user_info = []

#build the info list
def build_info_list():

    global passwd_file
    global shadow_file
    global user_info

    filp = open(passwd_file,"r")
    passwd_lines = filp.readlines()
    filp.close()
    filp = open(shadow_file, "r")
    shadow_lines = filp.readlines()
    filp.close()

    count=0
    for i,j in zip(passwd_lines,shadow_lines):
        pt = j.split(':')
        ut = i.split(':')
        user_info.append((ut[0],ut[2],ut[4],pt[1]))
        if count==58:
          break
        count +=1
    return user_info


# Create users and Change passwords
def add_ipa_users():

    global user_info
    cmd = 'ipa config-mod --enable-migration=true'
    os.system(cmd)

    for i in user_info:
        cmd="ipa user-add %s --first=%s --last=%s --uid=%s --email=%s --setattr userPassword='{CRYPT}%s'" % (i[0],i[0],i[0],i[1],i[2],i[3])
    #    print cmd
        os.system(cmd)

    cmd = 'ipa config-mod --enable-migration=false'
    os.system(cmd)

def main():
    build_info_list()
    add_ipa_users()

if __name__ == '__main__':
    main()

