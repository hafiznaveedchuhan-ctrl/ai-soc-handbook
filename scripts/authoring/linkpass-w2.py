"""Wave 2 link pass — appends a "## Related pages" section (before the footnotes).

  python3 -I scripts/authoring/linkpass-w2.py            # DRAFT pages only (safe any time)
  python3 -I scripts/authoring/linkpass-w2.py --stable   # also STABLE pages — run ONLY in the
                                                          # approval commit (body edit => re-approval,
                                                          # else ksor build refuses ksor-generated-stale)
Idempotent: links already present in a page are skipped; an existing "Related pages"
section is extended rather than duplicated.
"""
import glob, json, os, re, sys

R = {
 # false positives / owner policy
 "false-positives/expired-or-mistyped-passwords": ["windows-events/event-4625", "windows-events/event-4740", "playbooks/success-after-failures", "triage-note/example-false-positive", "linux-auth/ssh-failed-password", "orientation/glossary"],
 "false-positives/service-accounts": ["windows-events/event-4624", "windows-events/event-4625", "windows-events/event-4672", "mitre/t1078-valid-accounts", "wazuh/asset-and-user-context", "rules-map/escalation-policy"],
 "false-positives/backup-jobs": ["windows-events/event-4732", "windows-events/event-4728", "false-positives/service-accounts", "false-positives/admin-maintenance-windows", "wazuh/rule-levels"],
 "false-positives/admin-maintenance-windows": ["windows-events/event-1102", "playbooks/audit-log-cleared", "playbooks/new-service-or-scheduled-task", "windows-events/event-4720", "wazuh/rule-levels", "rules-map/severity-model"],
 "false-positives/vulnerability-scanners": ["mitre/t1046-network-service-discovery", "networking/ports-and-services", "networking/ids-ips", "networking/firewalls", "enrichment/private-ip-ranges", "false-positives/admin-maintenance-windows"],
 "sla/severity-response-matrix": ["rules-map/invariants", "triage-note/note-template", "orientation/glossary", "wazuh/rule-levels"],
 "wazuh/geo-and-vpn-caveats": ["networking/vpn-and-ipsec", "networking/proxies", "networking/nat-and-pat", "wazuh/alert-json-anatomy", "wazuh/asset-and-user-context", "mitre/t1078-valid-accounts"],
 "wazuh/asset-and-user-context": ["wazuh/alert-json-anatomy", "wazuh/architecture", "rules-map/escalation-policy", "rules-map/severity-model", "false-positives/backup-jobs"],
 # wazuh
 "wazuh/rule-groups": ["wazuh/rule-levels", "wazuh/windows-rules-reference", "wazuh/sshd-rules-reference", "wazuh/mitre-in-wazuh", "wazuh/alert-json-anatomy"],
 "wazuh/mitre-in-wazuh": ["wazuh/rule-groups", "wazuh/alert-json-anatomy", "mitre/t1110-brute-force", "mitre/t1078-valid-accounts"],
 "wazuh/sshd-rules-reference": ["linux-auth/ssh-failed-password", "linux-auth/ssh-invalid-user", "linux-auth/ssh-accepted", "wazuh/rule-groups", "playbooks/brute-force"],
 # linux auth
 "linux-auth/where-auth-logs-live": ["networking/syslog", "wazuh/architecture", "linux-auth/ssh-accepted", "linux-auth/sudo-usage", "wazuh/sshd-rules-reference"],
 "linux-auth/ssh-failed-password": ["wazuh/sshd-rules-reference", "linux-auth/ssh-invalid-user", "playbooks/brute-force", "mitre/t1110-001-password-guessing", "false-positives/expired-or-mistyped-passwords"],
 "linux-auth/ssh-invalid-user": ["linux-auth/ssh-failed-password", "mitre/t1110-003-password-spraying", "wazuh/sshd-rules-reference", "networking/remote-access-protocols"],
 "linux-auth/ssh-accepted": ["playbooks/success-after-failures", "mitre/t1078-valid-accounts", "networking/remote-access-protocols", "wazuh/geo-and-vpn-caveats"],
 "linux-auth/sudo-usage": ["linux-auth/where-auth-logs-live", "linux-auth/new-user-useradd", "mitre/t1548-002-bypass-uac", "rules-map/escalation-policy"],
 "linux-auth/new-user-useradd": ["windows-events/event-4720", "mitre/t1136-001-local-account", "playbooks/new-local-account", "linux-auth/sudo-usage"],
 # mitre
 "mitre/t1003-001-lsass-memory": ["sysmon/event-10-process-access", "sysmon/event-8-create-remote-thread", "mitre/t1078-valid-accounts", "rules-map/escalation-policy"],
 "mitre/t1021-001-remote-desktop-protocol": ["windows-events/event-4624", "windows-events/event-4648", "networking/remote-access-protocols", "mitre/t1078-valid-accounts"],
 "mitre/t1046-network-service-discovery": ["playbooks/port-scan", "networking/ports-and-services", "networking/network-attacks", "false-positives/vulnerability-scanners"],
 "mitre/t1053-005-scheduled-task": ["windows-events/event-4698", "playbooks/new-service-or-scheduled-task", "mitre/t1543-003-windows-service", "sysmon/event-1-process-create"],
 "mitre/t1110-004-credential-stuffing": ["mitre/t1110-brute-force", "mitre/t1110-001-password-guessing", "mitre/t1110-003-password-spraying", "playbooks/brute-force", "enrichment/ip-reputation-policy"],
 "mitre/t1543-003-windows-service": ["windows-events/event-7045", "windows-events/event-4697", "playbooks/new-service-or-scheduled-task", "sysmon/event-12-13-14-registry"],
 "mitre/t1548-002-bypass-uac": ["windows-events/event-4688", "windows-events/event-4672", "sysmon/event-1-process-create", "sysmon/event-12-13-14-registry"],
 "mitre/t1566-phishing": ["playbooks/suspicious-powershell", "sysmon/event-1-process-create", "sysmon/event-11-file-create", "networking/email-protocols"],
 "mitre/t1685-disable-or-modify-tools": ["mitre/t1685-005-clear-windows-event-logs", "windows-events/event-1102", "windows-events/event-4719", "playbooks/audit-log-cleared"],
 # playbooks
 "playbooks/account-lockout-storm": ["windows-events/event-4740", "windows-events/event-4625", "windows-events/event-4771", "false-positives/expired-or-mistyped-passwords", "false-positives/service-accounts", "mitre/t1110-003-password-spraying"],
 "playbooks/fim-or-malware-alert": ["sysmon/event-11-file-create", "sysmon/event-1-process-create", "false-positives/backup-jobs", "wazuh/rule-groups"],
 "playbooks/new-service-or-scheduled-task": ["windows-events/event-7045", "windows-events/event-4697", "windows-events/event-4698", "mitre/t1543-003-windows-service", "mitre/t1053-005-scheduled-task", "false-positives/admin-maintenance-windows"],
 "playbooks/port-scan": ["mitre/t1046-network-service-discovery", "false-positives/vulnerability-scanners", "networking/ports-and-services", "networking/tcp", "networking/firewalls", "enrichment/ip-reputation-policy"],
 "playbooks/suspicious-powershell": ["mitre/t1059-001-powershell", "windows-events/event-4688", "sysmon/event-1-process-create", "sysmon/event-3-network-connection", "mitre/t1566-phishing"],
 # sysmon
 "sysmon/overview": ["sysmon/event-1-process-create", "sysmon/event-3-network-connection", "sysmon/event-22-dns-query", "wazuh/architecture", "windows-events/event-4688"],
 "sysmon/event-1-process-create": ["windows-events/event-4688", "mitre/t1059-001-powershell", "playbooks/suspicious-powershell", "sysmon/overview"],
 "sysmon/event-3-network-connection": ["networking/tcp", "networking/ports-and-services", "enrichment/ip-reputation-policy", "sysmon/event-22-dns-query"],
 "sysmon/event-7-image-loaded": ["sysmon/event-1-process-create", "mitre/t1059-001-powershell", "sysmon/overview"],
 "sysmon/event-8-create-remote-thread": ["sysmon/event-10-process-access", "mitre/t1003-001-lsass-memory", "sysmon/overview"],
 "sysmon/event-10-process-access": ["mitre/t1003-001-lsass-memory", "sysmon/event-8-create-remote-thread", "rules-map/escalation-policy"],
 "sysmon/event-11-file-create": ["playbooks/fim-or-malware-alert", "mitre/t1566-phishing", "sysmon/event-1-process-create"],
 "sysmon/event-12-13-14-registry": ["mitre/t1543-003-windows-service", "windows-events/event-7045", "sysmon/overview"],
 "sysmon/event-22-dns-query": ["networking/dns", "sysmon/event-3-network-connection", "enrichment/ip-reputation-policy"],
 # windows events (Wave 2)
 "windows-events/event-4634": ["windows-events/event-4624", "windows-events/event-4672"],
 "windows-events/event-4697": ["windows-events/event-7045", "mitre/t1543-003-windows-service", "playbooks/new-service-or-scheduled-task"],
 "windows-events/event-4698": ["mitre/t1053-005-scheduled-task", "playbooks/new-service-or-scheduled-task", "false-positives/admin-maintenance-windows"],
 "windows-events/event-4719": ["windows-events/event-1102", "mitre/t1685-disable-or-modify-tools", "playbooks/audit-log-cleared"],
 "windows-events/event-4722": ["windows-events/event-4720", "windows-events/event-4725", "windows-events/event-4738", "mitre/t1098-account-manipulation"],
 "windows-events/event-4724": ["windows-events/event-4738", "windows-events/event-4720", "mitre/t1098-account-manipulation"],
 "windows-events/event-4725": ["windows-events/event-4722", "windows-events/event-4726", "windows-events/event-4738"],
 "windows-events/event-4726": ["windows-events/event-4720", "windows-events/event-4725", "playbooks/new-local-account"],
 "windows-events/event-4728": ["windows-events/event-4732", "windows-events/event-4756", "playbooks/added-to-admin-group", "rules-map/escalation-policy"],
 "windows-events/event-4738": ["windows-events/event-4720", "windows-events/event-4724", "mitre/t1098-account-manipulation"],
 "windows-events/event-4756": ["windows-events/event-4728", "windows-events/event-4732", "playbooks/added-to-admin-group"],
 "windows-events/event-4768": ["windows-events/event-4769", "windows-events/event-4771", "windows-events/event-4624"],
 "windows-events/event-4769": ["windows-events/event-4768", "windows-events/event-4624", "mitre/t1078-valid-accounts"],
 "windows-events/event-4771": ["windows-events/event-4625", "windows-events/event-4768", "windows-events/event-4776", "false-positives/expired-or-mistyped-passwords", "playbooks/account-lockout-storm"],
 "windows-events/event-4776": ["windows-events/event-4625", "windows-events/event-4771", "false-positives/expired-or-mistyped-passwords", "playbooks/brute-force"],
}
# Reverse links ONTO stable pages (applied only with --stable, in the approval commit).
S = {
 "windows-events/event-4625": ["windows-events/event-4771", "windows-events/event-4776", "false-positives/expired-or-mistyped-passwords", "playbooks/account-lockout-storm"],
 "windows-events/event-4624": ["windows-events/event-4634", "windows-events/event-4768", "false-positives/service-accounts", "mitre/t1021-001-remote-desktop-protocol"],
 "windows-events/event-4720": ["windows-events/event-4722", "windows-events/event-4726", "windows-events/event-4738", "linux-auth/new-user-useradd"],
 "windows-events/event-4732": ["windows-events/event-4728", "windows-events/event-4756"],
 "windows-events/event-4688": ["sysmon/event-1-process-create", "playbooks/suspicious-powershell"],
 "windows-events/event-1102": ["windows-events/event-4719", "mitre/t1685-disable-or-modify-tools", "false-positives/admin-maintenance-windows"],
 "windows-events/event-4740": ["playbooks/account-lockout-storm", "false-positives/expired-or-mistyped-passwords"],
 "windows-events/event-4672": ["windows-events/event-4634", "false-positives/backup-jobs"],
 "mitre/t1059-001-powershell": ["playbooks/suspicious-powershell", "sysmon/event-1-process-create"],
 "mitre/t1110-brute-force": ["mitre/t1110-004-credential-stuffing", "linux-auth/ssh-failed-password"],
 "playbooks/brute-force": ["linux-auth/ssh-failed-password", "playbooks/account-lockout-storm", "false-positives/expired-or-mistyped-passwords"],
 "rules-map/severity-model": ["sla/severity-response-matrix", "wazuh/asset-and-user-context"],
 "rules-map/escalation-policy": ["sla/severity-response-matrix", "false-positives/service-accounts"],
 "enrichment/ip-reputation-policy": ["wazuh/geo-and-vpn-caveats"],
 "wazuh/rule-levels": ["wazuh/rule-groups", "wazuh/mitre-in-wazuh"],
 "wazuh/alert-json-anatomy": ["wazuh/geo-and-vpn-caveats", "wazuh/asset-and-user-context"],
 "networking/vpn-and-ipsec": ["wazuh/geo-and-vpn-caveats"],
 "networking/ports-and-services": ["playbooks/port-scan", "mitre/t1046-network-service-discovery"],
 "networking/dns": ["sysmon/event-22-dns-query"],
 "networking/syslog": ["linux-auth/where-auth-logs-live"],
}

def title(p):
    t = re.search(r"^title: (.*)$", open(f"knowledge/{p}.md").read(), re.M).group(1).strip()
    return json.loads(t) if t.startswith('"') else t

def apply(src, targets):
    path = f"knowledge/{src}.md"; text = open(path).read()
    rel = lambda t: os.path.relpath(f"{t}.md", os.path.dirname(src))
    new = [t for t in targets if os.path.exists(f"knowledge/{t}.md") and t != src
           and f"]({rel(t)})" not in text]
    missing = [t for t in targets if not os.path.exists(f"knowledge/{t}.md")]
    assert not missing, (src, missing)
    if not new: return 0
    lines = "".join(f"- [{title(t)}]({rel(t)})\n" for t in new)
    m = re.search(r"^## Related pages\n\n((?:- .*\n)+)", text, re.M)
    if m:
        text = text[:m.end()] + lines + text[m.end():]
    else:
        f = re.search(r"^\[\^[^\]]+\]: ", text, re.M)
        cut = f.start() if f else len(text)
        text = text[:cut].rstrip() + "\n\n## Related pages\n\n" + lines + "\n" + text[cut:]
    open(path, "w").write(text); return len(new)

stable = "--stable" in sys.argv
n = 0
for src, tg in R.items():
    st = re.search(r"^status: (\w+)", open(f"knowledge/{src}.md").read(), re.M).group(1)
    if st == "stable" and not stable: continue
    n += apply(src, tg)
if stable:
    for src, tg in S.items(): n += apply(src, tg)
print(f"links added: {n}")
