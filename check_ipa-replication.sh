#!/bin/bash

# Replication Monitoring Nagios Plugin

RETVAL=3
RETSTAT=UNKNOWN
USERPASS="password"
DOMAIN="dc=example,dc=net"

if `ldapsearch -x -b "cn=mapping tree,cn=config" -D "uid=nagios,cn=users,cn=accounts,$DOMAIN" -w $USERPASS | grep nsds5replicaLastUpdateStatus | awk '$2 != 0 {exit 1}' > /dev/null 2>&1` ; then
    RETVAL=0
    RETSTAT=OK
else
    RETVAL=2
    RETSTAT=CRITICAL
fi

echo "$RETSTAT"
exit $RETVAL

