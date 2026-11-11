"""Retrieval polish + Wave 2 reverse links on STABLE pages — run ONLY after the owner says
"approved" for this change set (it re-stamps generated/approval on every touched page).

  python3 -I scripts/authoring/polish-stable.py --apply "<approval-at ISO Z>"
  python3 -I scripts/authoring/polish-stable.py --dry-run      # list what would change

Steps: (1) frontmatter/body edits below, (2) linkpass-w2.py --stable, (3) commit, (4) move
generated.at to that commit's time and approval.at to the given time on every touched page.
"""
import re, subprocess, sys

EDITS = {
 "knowledge/windows-events/event-4776.md": [
  ("0xC0000072 account disabled by administrator; 0xC0000193 expired account.[^ms-4776]",
   "0xC0000072 account disabled by administrator; 0xC0000193 expired account; 0xC0000071 expired password; 0xC0000224 \"Change Password at Next Logon\" flagged.[^ms-4776]"),
  ("| 0xC0000193 | Account expired |\n",
   "| 0xC0000193 | Account expired |\n| 0xC0000071 | Expired password — usually a support case ([expired or mistyped passwords](../false-positives/expired-or-mistyped-passwords.md)) |\n| 0xC0000224 | Must change password at next logon |\n"),
 ],
 "knowledge/rules-map/severity-model.md": [
  ("description: How the handbook rates an alert Low,",
   "description: How alert severity is decided — the handbook rates an alert Low,"),
 ],
 "knowledge/playbooks/added-to-admin-group.md": [
  ("description: L1 steps for event 4732 into the local Administrators group",
   "description: What to do when an account is added to the Administrators group — L1 steps for event 4732 into the local Administrators group"),
 ],
}

# Set 2 (prepared 2026-11-11 after evals on generation 6 — needs its OWN owner approval):
# the description edits above did not move retrieval, because search reads the text, not the
# description. These rename one heading per page so the text says what analysts ask.
EDITS2 = {
 "knowledge/rules-map/severity-model.md": [("\n## The model\n", "\n## How alert severity is decided\n")],
 "knowledge/playbooks/added-to-admin-group.md": [("\n## L1 steps\n", "\n## What to do when an account is added to Administrators (L1 steps)\n")],
}
if "--set2" in sys.argv: EDITS = EDITS2

def git(*a): return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout.strip()

def apply_edits():
    for p, pairs in EDITS.items():
        s = open(p).read()
        for a, b in pairs:
            if b in s: continue
            assert s.count(a) == 1, (p, a[:50]); s = s.replace(a, b)
        open(p, "w").write(s)
    if "--set2" not in sys.argv:
        subprocess.run([sys.executable, "-I", "scripts/authoring/linkpass-w2.py", "--stable"], check=True)

def restamp(paths, at):
    for p in paths:
        g = git("log", "-1", "--format=%cI", "--", p)
        gen = subprocess.run(["date", "-u", "-d", g, "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip()
        assert gen < at, (p, gen, at)
        s = open(p).read(); fm, body = s.split("\n---\n", 1)
        assert "status: stable" in fm, p
        fm = re.sub(r"^generated: \{ by: \"claude-opus/5.5\", at: [^ }]+ \}$", f'generated: {{ by: "claude-opus/5.5", at: {gen} }}', fm, flags=re.M)
        fm = re.sub(r"approval: \{ by: \"human:naveed\", at: [^ }]+ \}", f'approval: {{ by: "human:naveed", at: {at} }}', fm)
        open(p, "w").write(fm + "\n---\n" + body)

if "--dry-run" in sys.argv:
    apply_edits(); print(git("diff", "--stat")); git("checkout", "--", "knowledge"); sys.exit(0)
if "--apply" in sys.argv:
    at = sys.argv[sys.argv.index("--apply") + 1]
    apply_edits()
    touched = [l for l in git("diff", "--name-only").splitlines() if l.startswith("knowledge/")]
    git("add", *touched); git("commit", "-q", "-m", "Stable-page polish + Wave 2 reverse links (text), approved by human:naveed\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    if at == "now":
        import time; time.sleep(1)
        at = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip()
    restamp(touched, at); print("restamped", len(touched), "at", at)
