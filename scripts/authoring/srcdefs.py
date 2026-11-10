MS="https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing"
W="https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules"
G="https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows"
TOU="© The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation."
SRC={
 "naveed-interview-2026-11-10":("human:naveed interview 2026-11-10",'"human:naveed interview 2026-11-10"',"human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template)."),
 "nist-sp800-61r3":("NIST SP 800-61 Rev. 3 (April 2025)","https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf","NIST SP 800-61 Rev. 3 (April 2025), CSF elements RS.MA-02, RS.MA-03, RS.AN-03, DE.AE-08. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf"),
 "ms-4624":('"Microsoft Learn — 4624(S): An account was successfully logged on"',f"{MS}/event-4624",f'Microsoft Learn, "4624(S): An account was successfully logged on". {MS}/event-4624'),
 "ms-4625":('"Microsoft Learn — 4625(F): An account failed to log on"',f"{MS}/event-4625",f'Microsoft Learn, "4625(F): An account failed to log on". {MS}/event-4625'),
 "ms-4740":('"Microsoft Learn — 4740(S): A user account was locked out"',f"{MS}/event-4740",f'Microsoft Learn, "4740(S): A user account was locked out". {MS}/event-4740'),
 "ms-4720":('"Microsoft Learn — 4720(S): A user account was created"',f"{MS}/event-4720",f'Microsoft Learn, "4720(S): A user account was created". {MS}/event-4720'),
 "ms-4732":('"Microsoft Learn — 4732(S): A member was added to a security-enabled local group"',f"{MS}/event-4732",f'Microsoft Learn, "4732(S): A member was added to a security-enabled local group". {MS}/event-4732'),
 "ms-1102":('"Microsoft Learn — 1102(S): The audit log was cleared"',f"{MS}/event-1102",f'Microsoft Learn, "1102(S): The audit log was cleared". {MS}/event-1102'),
 "ms-4688":('"Microsoft Learn — 4688(S): A new process has been created"',f"{MS}/event-4688",f'Microsoft Learn, "4688(S): A new process has been created". {MS}/event-4688'),
 "mitre-t1110":("MITRE ATT&CK — T1110 Brute Force","https://attack.mitre.org/techniques/T1110/",f'MITRE ATT&CK, "Brute Force, Technique T1110". {TOU} https://attack.mitre.org/techniques/T1110/'),
 "mitre-t1078":("MITRE ATT&CK — T1078 Valid Accounts","https://attack.mitre.org/techniques/T1078/",f'MITRE ATT&CK, "Valid Accounts, Technique T1078". {TOU} https://attack.mitre.org/techniques/T1078/'),
 "mitre-t1136-001":('"MITRE ATT&CK — T1136.001 Create Account: Local Account"',"https://attack.mitre.org/techniques/T1136/001/",f'MITRE ATT&CK, "Create Account: Local Account, Sub-technique T1136.001". {TOU} https://attack.mitre.org/techniques/T1136/001/'),
 "mitre-t1098":("MITRE ATT&CK — T1098 Account Manipulation","https://attack.mitre.org/techniques/T1098/",f'MITRE ATT&CK, "Account Manipulation, Technique T1098". {TOU} https://attack.mitre.org/techniques/T1098/'),
 "mitre-t1685-005":('"MITRE ATT&CK — T1685.005 Disable or Modify Tools: Clear Windows Event Logs"',"https://attack.mitre.org/techniques/T1685/005/",f'MITRE ATT&CK, "Disable or Modify Tools: Clear Windows Event Logs, Sub-technique T1685.005". {TOU} https://attack.mitre.org/techniques/T1685/005/'),
 "wazuh-0580":("Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml",f"{W}/0580-win-security_rules.xml",f"Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. {W}/0580-win-security_rules.xml"),
 "wazuh-0610":("Wazuh ruleset v4.14.10 — 0610-win-ms_logs_rules.xml",f"{W}/0610-win-ms_logs_rules.xml",f"Wazuh ruleset, tag v4.14.10, `ruleset/rules/0610-win-ms_logs_rules.xml`, rule 63103. {W}/0610-win-ms_logs_rules.xml"),
 "wazuh-poc-bf":("\"Wazuh documentation — PoC: Detecting a brute-force attack\"","https://documentation.wazuh.com/current/proof-of-concept-guide/detect-brute-force-attack.html",'Wazuh documentation, "Detecting a brute-force attack" (proof-of-concept guide). https://documentation.wazuh.com/current/proof-of-concept-guide/detect-brute-force-attack.html'),
 "abuseipdb-docs":("AbuseIPDB APIv2 documentation","https://docs.abuseipdb.com/","AbuseIPDB, \"APIv2 documentation\". https://docs.abuseipdb.com/"),
 "sigma-user-creation":("SigmaHQ — Local User Creation (r2026-07-01)",f"{G}/builtin/security/win_security_user_creation.yml",f'SigmaHQ, "Local User Creation", release r2026-07-01 (secondary source). {G}/builtin/security/win_security_user_creation.yml'),
 "sigma-user-added-local-admins":("SigmaHQ — User Added to Local Administrator Group (r2026-07-01)",f"{G}/builtin/security/win_security_user_added_to_local_administrators.yml",f'SigmaHQ, "User Added to Local Administrator Group", release r2026-07-01 (secondary source). {G}/builtin/security/win_security_user_added_to_local_administrators.yml'),
 "sigma-audit-log-cleared":("SigmaHQ — Security Eventlog Cleared (r2026-07-01)",f"{G}/builtin/security/win_security_audit_log_cleared.yml",f'SigmaHQ, "Security Eventlog Cleared", release r2026-07-01 (secondary source). {G}/builtin/security/win_security_audit_log_cleared.yml'),
}
def page(path, typ, title, desc, order, ids, body):
    fm=["---",f"type: {typ}",f'title: "{title}"',f"description: {desc}","status: draft",f"order: {order}","sources:"]
    for i in ids:
        t,r,_=SRC[i]; fm+= [f"  - id: {i}",f"    title: {t}",f"    resource: {r}"]
    fm+=["ksor:","  audience: [public]","  owner: human:naveed","---",""]
    foot="\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids)
    open(path,"w").write("\n".join(fm)+body.strip()+"\n\n"+foot+"\n")
