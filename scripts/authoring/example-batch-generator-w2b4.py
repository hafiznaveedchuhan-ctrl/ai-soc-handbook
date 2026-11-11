"""Wave 2 batch B4 — linux-auth (6) + wazuh (3). Drafts. Sources fetched 2026-11-11."""
import os, json
W = "https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules"
D = "https://documentation.wazuh.com/current/user-manual"
SRC = {
 "wazuh-0095": ("Wazuh ruleset v4.14.10 — 0095-sshd_rules.xml", f"{W}/0095-sshd_rules.xml", f"Wazuh ruleset, tag v4.14.10, `ruleset/rules/0095-sshd_rules.xml`. {W}/0095-sshd_rules.xml"),
 "wazuh-0020": ("Wazuh ruleset v4.14.10 — 0020-syslog_rules.xml", f"{W}/0020-syslog_rules.xml", f"Wazuh ruleset, tag v4.14.10, `ruleset/rules/0020-syslog_rules.xml`. {W}/0020-syslog_rules.xml"),
 "wazuh-rules-xml": ('"Wazuh documentation — Rules syntax"', f"{D}/ruleset/ruleset-xml-syntax/rules.html", f'Wazuh documentation, "Rules" (ruleset XML syntax: group, if_group, frequency, timeframe, ignore). {D}/ruleset/ruleset-xml-syntax/rules.html'),
 "wazuh-mitre": ('"Wazuh documentation — MITRE ATT&CK framework"', f"{D}/ruleset/mitre.html", f'Wazuh documentation, "MITRE ATT&CK framework". {D}/ruleset/mitre.html'),
 "wazuh-logcollect": ('"Wazuh documentation — Configuring log collection for different operating systems"', f"{D}/capabilities/log-data-collection/configuration.html", f'Wazuh documentation, "Configuring log collection for different operating systems" (Linux). {D}/capabilities/log-data-collection/configuration.html'),
 "ubuntu-rsyslog": ("Ubuntu rsyslog package — debian/50-default.conf", "https://git.launchpad.net/ubuntu/+source/rsyslog/plain/debian/50-default.conf", "Ubuntu rsyslog source package, `debian/50-default.conf`. https://git.launchpad.net/ubuntu/+source/rsyslog/plain/debian/50-default.conf"),
 "redhat-rsyslog": ("rsyslog project — platform/redhat/rsyslog.conf", "https://raw.githubusercontent.com/rsyslog/rsyslog/main/platform/redhat/rsyslog.conf", "rsyslog project, `platform/redhat/rsyslog.conf` (Red Hat default). https://raw.githubusercontent.com/rsyslog/rsyslog/main/platform/redhat/rsyslog.conf"),
 "sshd-config": ("OpenBSD manual — sshd_config(5)", "https://man.openbsd.org/sshd_config.5", "OpenBSD manual page `sshd_config(5)` (SyslogFacility, LogLevel). https://man.openbsd.org/sshd_config.5"),
}
def page(path, typ, title, desc, order, ids, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fm = ["---", f"type: {typ}", f'title: "{title}"', "description: " + json.dumps(desc, ensure_ascii=False), "status: draft", f"order: {order}", "sources:"]
    for i in ids:
        t, r, _ = SRC[i]; fm += [f"  - id: {i}", f"    title: {t}", f"    resource: {r}"]
    fm += ["ksor:", "  audience: [public]", "  owner: human:naveed", "---", ""]
    miss = [i for i in ids if f"[^{i}]" not in body]; assert not miss, (path, miss)
    open(path, "w").write("\n".join(fm) + body.strip() + "\n\n" + "\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids) + "\n")

L = "knowledge/linux-auth"
page(f"{L}/where-auth-logs-live.md", "Definition", "Where Linux authentication logs live",
"Which file holds SSH, sudo and login events on Debian/Ubuntu (/var/log/auth.log) and Red Hat (/var/log/secure), why sshd writes to the AUTH facility, and how those logs reach Wazuh.", 500,
["ubuntu-rsyslog", "redhat-rsyslog", "sshd-config", "wazuh-logcollect"], """
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
""")

page(f"{L}/ssh-failed-password.md", "Definition", "SSH failed password",
"What an sshd authentication failure looks like to Wazuh (rules 5716, 5760), when repeated failures become a brute-force alert (5720, 5763: 8 from one source), and how to triage it.", 510,
["wazuh-0095", "wazuh-rules-xml"], """
> [!NOTE]
> **In plain words.** Someone tried to log in over SSH and the password (or
> other method) was wrong. One failure is normal; many from the same address
> in a short time is guessing.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5716 | 5 | lines starting `Failed` or `error: PAM: Authentication` | sshd: authentication failed |
| 5760 | 5 | `Failed password`, `Failed keyboard`, `authentication error` | sshd: authentication failed |
| 5720 | 10 | 5716 seen 8 times, same source IP | Multiple authentication failures |
| 5763 | 10 | 5760 seen 8 times in 120 s, same source IP (then ignored 60 s) | brute force — authentication failed |

All rows: [^wazuh-0095]

- `frequency` is how many times a rule must match before alerting, `timeframe` is the window in seconds, and `ignore` suppresses the rule for that many seconds after it fires.[^wazuh-rules-xml]
- MITRE tags in the ruleset: 5716 → T1110; 5760 → T1110.001 and T1021.004.[^wazuh-0095]

## For the agent

| Signal | Next action |
|---|---|
| Single 5716/5760 | Note; usually a user typo |
| 5720 or 5763 | Brute force from one source — see the [brute-force playbook](../playbooks/brute-force.md) |
| Followed by [SSH accepted](ssh-accepted.md) from the same IP | Escalate per escalation policy |
""")

page(f"{L}/ssh-accepted.md", "Definition", "SSH accepted (successful login)",
"How Wazuh records a successful SSH login (rule 5715, level 3, mapped to T1078 and T1021), and when a normal-looking success is the most important line in a brute-force story.", 511,
["wazuh-0095"], """
> [!NOTE]
> **In plain words.** Someone logged in over SSH successfully. Usually normal —
> unless the same address was failing a moment earlier.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5715 | 3 | lines starting `Accepted` or ending `authenticated.` | sshd: authentication success |

Row: [^wazuh-0095]

- MITRE tags in the ruleset: T1078 (Valid Accounts) and T1021 (Remote Services).[^wazuh-0095]

## For the agent

| Signal | Next action |
|---|---|
| 5715 after 5720/5763 from the same IP | Success after brute force — escalate (see [success after failures](../playbooks/success-after-failures.md)) |
| 5715 for `root` or from a public IP | Check whether that is expected for this host |
| 5715 at an unusual time for the user | Note in the triage note |
""")

page(f"{L}/ssh-invalid-user.md", "Definition", "SSH invalid (non-existent) user",
"Wazuh rules 5710 and 5712 for SSH attempts against usernames that do not exist, and 5718/5719 for denied users — the clearest sign of automated username guessing.", 512,
["wazuh-0095"], """
> [!NOTE]
> **In plain words.** Someone tried to log in with a username that does not
> exist on the server. Real users rarely do this; scripts guessing common names
> (admin, test, oracle…) do it constantly.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5710 | 5 | `illegal user` or `invalid user` | Attempt to login using a non-existent user |
| 5712 | 10 | 5710 seen 8 times in 120 s, same source IP | brute force — non-existent user |
| 5718 | 5 | `not allowed because` | Attempt to login using a denied user |
| 5719 | 10 | repeated 5718 | Multiple access attempts using a denied user |

All rows: [^wazuh-0095]

- MITRE tags: 5710 → T1110.001 and T1021.004; 5712, 5718, 5719 → T1110.[^wazuh-0095]

## For the agent

| Signal | Next action |
|---|---|
| 5712 from a public IP | Automated guessing — brute-force playbook; check for any 5715 from that IP |
| 5710 for a name that looks like a real employee | Possible targeted attempt — note it |
""")

page(f"{L}/sudo-usage.md", "Definition", "sudo usage",
"How Wazuh classifies sudo events — failed password (5401), three failures (5404), user not in sudoers (5405), successful sudo to root (5402) and first-time sudo (5403) — all mapped to T1548.003.", 520,
["wazuh-0020"], """
> [!NOTE]
> **In plain words.** `sudo` runs a command with higher rights. Failed sudo
> passwords, users who are not allowed to sudo, and someone using sudo for the
> very first time are all worth a look.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5401 | 5 | `incorrect password attempt` | Failed attempt to run sudo |
| 5404 | 10 | `3 incorrect password attempts` | Three failed attempts to run sudo |
| 5405 | 5 | `user NOT in sudoers` | Unauthorized user attempted to use sudo |
| 5402 | 3 | `USER=root ; COMMAND=` | Successful sudo to ROOT executed |
| 5407 | 3 | `USER=<any> ; COMMAND=` | Successful sudo executed |
| 5403 | 4 | first time seen for this user | First time user executed sudo |

All rows: [^wazuh-0020]

- All are tagged MITRE T1548.003 in the ruleset.[^wazuh-0020]

## For the agent

| Signal | Next action |
|---|---|
| 5405 | A user tried sudo without permission — check the account and command |
| 5404 | Repeated wrong sudo password — check for a stolen session |
| 5403 for a service or new account | Unexpected first sudo — escalate per policy |
""")

page(f"{L}/new-user-useradd.md", "Definition", "New Linux user or group (useradd, gpasswd)",
"Wazuh rules for account changes on Linux — new user (5902, T1136), new group (5901), useradd failed (5905), user added to a group (2960) and to the sudo group (2961).", 530,
["wazuh-0020"], """
> [!NOTE]
> **In plain words.** A new user account or group appeared on a Linux server,
> or someone was added to the `sudo` group. Attackers create accounts to keep
> access.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5902 | 8 | `new user` / `new account added` | New user added to the system (T1136) |
| 5901 | 8 | `new group` | New group added to the system |
| 5905 | 0 | `useradd` … `failed adding user` | useradd failed |
| 2960 | 2 | gpasswd `added by` | User added to group (T1136) |
| 2961 | 5 | group field = `sudo` | User added to group sudo (T1136) |

All rows: [^wazuh-0020]

See also the Windows counterpart [4720](../windows-events/event-4720.md) and the [new local account playbook](../playbooks/new-local-account.md).

## For the agent

| Signal | Next action |
|---|---|
| 5902 outside a change window | Ask who created it; check for a following SSH login |
| 2961 (added to sudo) | Privilege change — escalate per policy |
""")

Z = "knowledge/wazuh"
page(f"{Z}/rule-groups.md", "Definition", "Wazuh rule groups",
"What the <group> element in a Wazuh rule is, how to filter alerts by rule.groups, the authentication groups the sshd rules use, and how if_group and frequency/timeframe build correlation rules.", 604,
["wazuh-rules-xml", "wazuh-0095"], """
> [!NOTE]
> **In plain words.** Every Wazuh rule carries one or more group labels, such
> as `authentication_failed`. Groups let you search for a whole family of
> alerts at once, and let one rule react to another.

## What a group is

- Groups categorise alerts and allow filtering related alerts in the dashboard, e.g. `rule.groups: attack` or `rule.groups: (syscheck OR syslog)`.[^wazuh-rules-xml]
- `if_group` makes a rule match only when a rule of that group matched; `if_matched_group` adds "within a period of time".[^wazuh-rules-xml]
- `frequency` (2–9999) is how many matches are needed, `timeframe` (seconds) the window, `ignore` (seconds) the quiet time after firing.[^wazuh-rules-xml]

## Groups in the SSH rules

| Group | Example rules |
|---|---|
| `syslog`, `sshd` | every rule in the sshd file |
| `authentication_failed` | 5710, 5716, 5760 |
| `authentication_success` | 5715 |
| `authentication_failures` | 5712, 5720, 5763 |

All rows: [^wazuh-0095]

The same rules also carry compliance groups (for example `pci_dss_10.2.4`, `nist_800_53_AC.7`).[^wazuh-0095]

## For the agent

| Question | Query |
|---|---|
| All failed logins | `rule.groups: authentication_failed` |
| All brute-force correlations | `rule.groups: authentication_failures` |
""")

page(f"{Z}/sshd-rules-reference.md", "Definition", "Wazuh sshd rules reference",
"One table of the Wazuh v4.14.10 sshd rules an L1 analyst meets — level, what they match, frequency settings and MITRE tags — with links to the Linux auth pages that explain each.", 605,
["wazuh-0095"], """
> [!NOTE]
> **In plain words.** The quick lookup for SSH alerts: find the rule ID from
> the alert, read its level and meaning here, then open the linked page.

| Rule | Level | Meaning | Correlation | MITRE | Page |
|---|---|---|---|---|---|
| 5700 | 0 | SSHD messages grouped (parent) | — | — | — |
| 5701 | 8 | Possible attack on the ssh server (version gathering) | — | T1190 | — |
| 5704 | 4 | Timeout while logging in | — | — | — |
| 5705 | 10 | Possible scan or breakin (many login timeouts) | on 5704 | T1190, T1110 | — |
| 5706 | 6 | Insecure connection attempt (scan) | — | T1021.004 | — |
| 5710 | 5 | Login with a non-existent user | — | T1110.001, T1021.004 | [Invalid user](../linux-auth/ssh-invalid-user.md) |
| 5712 | 10 | Brute force, non-existent user | 8 in 120 s, same IP | T1110 | [Invalid user](../linux-auth/ssh-invalid-user.md) |
| 5715 | 3 | Authentication success | — | T1078, T1021 | [Accepted](../linux-auth/ssh-accepted.md) |
| 5716 | 5 | Authentication failed | — | T1110 | [Failed password](../linux-auth/ssh-failed-password.md) |
| 5718 | 5 | Login with a denied user | — | T1110 | [Invalid user](../linux-auth/ssh-invalid-user.md) |
| 5720 | 10 | Multiple authentication failures | 8 × 5716, same IP | T1110 | [Failed password](../linux-auth/ssh-failed-password.md) |
| 5731 | 6 | SSH scanning | — | T1046 | — |
| 5758 | 8 | Maximum authentication attempts exceeded | — | T1110 | — |
| 5760 | 5 | Authentication failed | — | T1110.001, T1021.004 | [Failed password](../linux-auth/ssh-failed-password.md) |
| 5763 | 10 | Brute force, authentication failed | 8 in 120 s, same IP | T1110 | [Failed password](../linux-auth/ssh-failed-password.md) |

All rows: [^wazuh-0095]
""")

page(f"{Z}/mitre-in-wazuh.md", "Standard", "MITRE ATT&CK in Wazuh",
"How Wazuh maps alerts to MITRE ATT&CK — rule <mitre> IDs, the rule.mitre fields in an alert, the dashboard module's Framework, Dashboard and Intelligence tabs — and how to use the mapping in triage without over-trusting it.", 606,
["wazuh-mitre", "wazuh-0095"], """
> [!NOTE]
> **In plain words.** Many Wazuh rules carry a MITRE technique ID. The alert
> then tells you which attacker behaviour the rule *might* indicate. It is a
> label from the rule writer, not proof.

## How the mapping works

- Wazuh ships detection rules mapped to MITRE IDs, and custom rules can be given IDs too.[^wazuh-mitre]
- The dashboard's MITRE ATT&CK module maps alerts to tactics and techniques; its **Framework** tab shows techniques seen per endpoint, the **Dashboard** tab totals and the top 10 TTPs, and the **Intelligence** tab threat actors, IOCs and mitigations.[^wazuh-mitre]
- Example from the ruleset: sshd rule 5760 carries T1110.001 and T1021.004; 5715 (success) carries T1078 and T1021.[^wazuh-0095]
- The alert JSON fields are explained in [Alert JSON anatomy](alert-json-anatomy.md).

## For the agent

| Use | Do |
|---|---|
| Name the technique in the triage note | Use the alert's MITRE ID and link the handbook page if one exists ([mitre/](../mitre/t1110-brute-force.md)) |
| Decide severity | Do **not** decide on the MITRE tag alone — use the [severity model](../rules-map/severity-model.md) |
""")
print("ok")
