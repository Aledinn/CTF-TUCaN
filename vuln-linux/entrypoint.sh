#!/bin/sh

# Make database credentials available only to commands running as root.
printf '%s:%s:%s:%s:%s\n' "$PGHOST" "5432" "$PGDATABASE" "$PGUSER" "$PGPASSWORD" > /root/.pgpass
chmod 600 /root/.pgpass
unset PGPASSWORD

# Ensure /etc/shadow is readable only by root
chmod 640 /etc/shadow
chown root:shadow /etc/shadow

exec /usr/sbin/sshd -D
