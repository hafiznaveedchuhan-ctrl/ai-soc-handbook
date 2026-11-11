"""Stamp draft pages stable after the owner's explicit approval.
Usage: python3 -I scripts/authoring/approve-pages.py "<approval-at ISO Z>" page.md [...]
generated.at = last commit time of the page body (UTC); approval.at must be later."""
import re, subprocess, sys
at = sys.argv[1]
for p in sys.argv[2:]:
    t = open(p).read(); fm, body = t.split("\n---\n", 1)
    assert "status: draft" in fm, p
    g = subprocess.run(["git", "log", "-1", "--format=%cI", "--", p], capture_output=True, text=True).stdout.strip()
    gen = subprocess.run(["date", "-u", "-d", g, "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip()
    assert gen and gen < at, (p, gen)
    fm = fm.replace("status: draft", "status: stable")
    fm = re.sub(r"^(order: .*)$", r'\1\ngenerated: { by: "claude-opus/5.5", at: ' + gen + " }", fm, count=1, flags=re.M)
    fm = fm.replace("  owner: human:naveed", '  owner: human:naveed\n  approval: { by: "human:naveed", at: ' + at + " }")
    assert fm.count("approval:") == 1 and fm.count("generated:") == 1, p
    open(p, "w").write(fm + "\n---\n" + body)
print("stamped", len(sys.argv) - 2)
