#!/usr/bin/python -tt
# This is a Free and Open Source Software
# Copyright chandank.kumar@gmail.com

import sys
import os

user_file = 'user.list'

# Read the file
def read_user_file():
    filp = open(user_file,"r")
    user_lines = filp.readlines()
    filp.close()
    return user_lines

#build the info list
def build_info_list(user_lines):
    user_info = []
    for i in user_lines:
        user_info.append(i.split())
    return user_info

# Create users and Change passwords
def add_ipa_users(user_info):
    count=0
    for i in user_info:
        count +=1
        cmd="ipa user-add %s --first=%s --last=%s --uid=%s --setattr userPassword=%s" % (i[0],i[1],i[2],i[3],i[4])
        print cmd
        if count == 5:
          break
        #print "ipa user-add %s --first= --last= --uid= --setattr userPassword=" % (i)
        #os.system(cmd)
def main():
    user_lines = read_user_file()
    user_info = build_info_list(user_lines)
    add_ipa_users(user_info)

if __name__ == '__main__':
    main()
