
FROM rockylinux:9


RUN dnf install -y \
    openssh-server sudo shadow-utils bash procps-ng iproute \
    && dnf clean all


RUN useradd -m -s /bin/bash ops \
    && usermod -p '*' ops \
    && mkdir -p /home/ops/.ssh /run/sshd \
    && printf 'ops ALL=(ALL:ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/ops \
    && chmod 0440 /etc/sudoers.d/ops \
    && visudo -cf /etc/sudoers.d/ops


COPY ssh/authorized_keys /home/ops/.ssh/authorized_keys
COPY server-info.sh /usr/local/bin/server-info.sh

RUN chown -R ops:ops /home/ops/.ssh \
    && chmod 700 /home/ops/.ssh \
    && chmod 600 /home/ops/.ssh/authorized_keys \
    && chmod 755 /usr/local/bin/server-info.sh \
    && ssh-keygen -A \
    && printf 'Port 22\nPermitRootLogin no\nPubkeyAuthentication yes\nPasswordAuthentication no\nKbdInteractiveAuthentication no\nAuthorizedKeysFile .ssh/authorized_keys\nAllowUsers ops\nUsePAM no\n' > /etc/ssh/sshd_config

EXPOSE 22

CMD ["/bin/sh", "-c", "mkdir -p /run/sshd && ssh-keygen -A && exec /usr/sbin/sshd -D -e"]
