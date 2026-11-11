---
type: Definition
title: "Active Directory basics"
description: "What Active Directory Domain Services stores, what domain controllers do, how Kerberos and NTLM authenticate users, and which admin groups matter most to a SOC analyst."
status: draft
order: 1406
sources:
  - id: ms-adds
    title: "Microsoft Learn — Active Directory Domain Services overview"
    resource: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview
  - id: ms-kerberos
    title: "Microsoft Learn — Kerberos authentication overview"
    resource: https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview
  - id: ms-ntlm
    title: "Microsoft Learn — NTLM overview"
    resource: https://learn.microsoft.com/en-us/windows-server/security/kerberos/ntlm-overview
  - id: ms-security-groups
    title: "Microsoft Learn — Active Directory security groups"
    resource: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Active Directory is the central phone book and gatekeeper
> of a Windows network: it holds every user and computer account, and its
> domain controllers decide who may log in.

## What AD DS is

- A directory is a hierarchical structure that stores information about objects
  on a network; AD DS stores them — servers, volumes, printers, user and
  computer accounts — and makes them available to users and admins.[^ms-adds]
- It includes a **schema** (the rules for object classes and attributes), a
  **global catalog** (information about every object in the directory), a query
  and index mechanism, and **replication**: every domain controller in a domain
  holds a complete copy of the domain's directory, and changes replicate to all
  of them.[^ms-adds]

## Kerberos — the default

- Three parties: the client, the service, and the **Key Distribution Center
  (KDC)**, which runs on every domain controller and uses the AD DS database.[^ms-kerberos]
- At sign-in the client gets a **ticket-granting ticket (TGT)** from the KDC
  ([event 4768](../windows-events/event-4768.md)); to reach a service it
  presents the TGT and gets a **service ticket** ([event 4769](../windows-events/event-4769.md)).[^ms-kerberos]
- Kerberos gives mutual authentication; NTLM does not let a client verify a
  server's identity.[^ms-kerberos]

## NTLM — still around

- A family of challenge-response protocols (LAN Manager v1/v2, NTLM v1/v2).[^ms-ntlm]
- Still required for workgroup systems and used for local logon on
  non-domain-controllers; Kerberos v5 is the preferred method in AD, but
  applications may still use NTLM.[^ms-ntlm]
- NTLM validation on a domain controller is [event 4776](../windows-events/event-4776.md).

## Admin groups to watch

| Group | Why it matters |
|---|---|
| Domain Admins | Authorised to administer the domain; by default a member of Administrators on every domain-joined computer, including DCs |
| Enterprise Admins | Exists only in the forest root domain; authorised to make forest-wide changes such as adding child domains |

Rows: [^ms-security-groups]

Group scopes are universal, global and domain local; built-in groups have
Builtin Local scope.[^ms-security-groups] Membership changes are
[4728](../windows-events/event-4728.md) (global),
[4756](../windows-events/event-4756.md) (universal) and
[4732](../windows-events/event-4732.md) (local).

## Related pages

- [Event 4771: Kerberos pre-authentication failed](../windows-events/event-4771.md)
- [Playbook: account added to Administrators](../playbooks/added-to-admin-group.md)
- [False positives: service accounts](../false-positives/service-accounts.md)

[^ms-adds]: Microsoft Learn, "Active Directory Domain Services overview". https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview
[^ms-kerberos]: Microsoft Learn, "Kerberos authentication overview" (last updated 2026-09-15). https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview
[^ms-ntlm]: Microsoft Learn, "NTLM overview". https://learn.microsoft.com/en-us/windows-server/security/kerberos/ntlm-overview
[^ms-security-groups]: Microsoft Learn, "Active Directory security groups". https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups
