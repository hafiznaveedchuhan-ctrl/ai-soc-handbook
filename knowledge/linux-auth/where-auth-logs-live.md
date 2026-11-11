---
type: Definition
title: "Where Linux authentication logs live"
description: "Which file holds SSH, sudo and login events on Debian/Ubuntu (/var/log/auth.log) and Red Hat (/var/log/secure), why sshd writes to the AUTH facility, and how those logs reach Wazuh."
status: draft
order: 500
sources:
  - id: ubuntu-rsyslog
    title: Ubuntu rsyslog package — debian/50-default.conf
    resource: https://git.launchpad.net/ubuntu/+source/rsyslog/plain/debian/50-default.conf
  - id: redhat-rsyslog
    title: rsyslog project — platform/redhat/rsyslog.conf
    resource: https://raw.githubusercontent.com/rsyslog/rsyslog/main/platform/redhat/rsyslog.conf
  - id: sshd-config
    title: OpenBSD manual — sshd_config(5)
    resource: https://man.openbsd.org/sshd_config.5
  - id: wazuh-logcollect
    title: "Wazuh documentation — Configuring log collection for different operating systems"
    resource: https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** On Linux, SSH logins, sudo and new-user events go to a
> special "auth" log file. Its name depends on the distribution. If the alert
> mentions SSH or sudo, this file is where the original line lives.

## The file, by distribution

| Distribution family | File | Default rule |
|---|---|---|
| Debian / Ubuntu | `/var/log/auth.log` | `auth,authpriv.*  /var/log/auth.log`[^ubuntu-rsyslog] |
| Red Hat family | `/var/log/secure` | `authpriv.*  /var/log/secure`[^redhat-rsyslog] |

- On Red Hat the general `/var/log/messages` excludes `authpriv` messages; the comment in the file says private authentication messages are kept out of it.[^redhat-rsyslog]
- `sshd` logs with the syslog facility set by `SyslogFacility`; the default is **AUTH**. `LogLevel` sets how much it writes.[^sshd-config]

## Getting them into Wazuh

- The Wazuh agent collects and forwards Linux events; a Linux host can also forward events over syslog (rsyslog) to the Wazuh server, which listens with a `<remote>` syslog block (port 514, tcp or udp, allowed IPs).[^wazuh-logcollect]

## For the agent

| Question | Answer |
|---|---|
| Alert is about SSH/sudo on Ubuntu | Original line is in `/var/log/auth.log` |
| Same on RHEL/CentOS/Rocky | `/var/log/secure` |
| No auth events from a host | Check that the agent or rsyslog forwarding is running |

## Related pages

- [Syslog](../networking/syslog.md)
- [Wazuh architecture](../wazuh/architecture.md)
- [SSH accepted (successful login)](ssh-accepted.md)
- [sudo usage](sudo-usage.md)
- [Wazuh sshd rules reference](../wazuh/sshd-rules-reference.md)

[^ubuntu-rsyslog]: Ubuntu rsyslog source package, `debian/50-default.conf`. https://git.launchpad.net/ubuntu/+source/rsyslog/plain/debian/50-default.conf
[^redhat-rsyslog]: rsyslog project, `platform/redhat/rsyslog.conf` (Red Hat default). https://raw.githubusercontent.com/rsyslog/rsyslog/main/platform/redhat/rsyslog.conf
[^sshd-config]: OpenBSD manual page `sshd_config(5)` (SyslogFacility, LogLevel). https://man.openbsd.org/sshd_config.5
[^wazuh-logcollect]: Wazuh documentation, "Configuring log collection for different operating systems" (Linux). https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html
