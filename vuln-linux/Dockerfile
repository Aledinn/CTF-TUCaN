FROM ubuntu:22.04

RUN apt update && apt install -y \
    openssh-server \
    sudo \
    postgresql-client \
    net-tools \
    procps

RUN apt install -y gcc

#SUID binary
COPY legacy_check.c /tmp/legacy_check.c
RUN gcc /tmp/legacy_check.c -o /usr/local/bin/legacy_check && \
    chown root:root /usr/local/bin/legacy_check && \
    chmod 4755 /usr/local/bin/legacy_check

#users
RUN useradd -m tu27bd3d10Da && echo "tu27bd3d10Da:legacy123" | chpasswd
RUN useradd -m admin123 && echo "admin123:admin123" | chpasswd

#ssh
RUN mkdir /var/run/sshd

# Sudo misconfig
RUN echo "admin123 ALL=(root) NOPASSWD: /usr/bin/psql" >> /etc/sudoers

# Disable root SSH
RUN sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
