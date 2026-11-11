"""Pre-check quiz YAML files against the same thresholds as system/site/lib/quiz-audit.ts.
Usage: python3 -I scripts/authoring/quiz_precheck.py knowledge/**/*.quiz.yaml
Rules mirrored: answer-position share <= 60%, longest/shortest-unique-option strategy wins <= 60%,
no run of more than 3 identical answers, no duplicate 60-char stems (ratio rules need >= 5 questions)."""
import sys, re, itertools, collections, json
def load(p):
    qs=[]; cur=None
    for line in open(p, encoding='utf-8'):
        m=re.match(r'\s*- question:\s*(.*)',line)
        if m: cur={'q':json.loads(m.group(1)),'o':[],'a':None}; qs.append(cur); continue
        if cur is None: continue
        m=re.match(r'\s{6}- (".*")\s*$',line)
        if m: cur['o'].append(json.loads(m.group(1))); continue
        m=re.match(r'\s*answer:\s*(\d+)',line)
        if m: cur['a']=int(m.group(1))
    return qs
def pick(opts,want):
    L=[len(o) for o in opts]; t=max(L) if want=='long' else min(L); h=[i for i,l in enumerate(L) if l==t]
    return h[0] if len(h)==1 else None
bad=0
for p in sys.argv[1:]:
    qs=load(p); n=len(qs); ans=[q['a'] for q in qs]; issues=[]
    if n>=5:
        if max(collections.Counter(ans).values())/n>0.6: issues.append('answer-bias')
        for w in ('long','short'):
            if sum(1 for q in qs if pick(q['o'],w)==q['a'])/n>0.6: issues.append(f'length-bias-{w}')
    if n and max(len(list(g)) for _,g in itertools.groupby(ans))>3: issues.append('answer-run')
    stems=[q['q'].strip()[:60].lower() for q in qs]
    if len(stems)!=len(set(stems)): issues.append('duplicate-stem')
    print(('FIX ' if issues else 'ok  ')+p, ','.join(issues)); bad+=bool(issues)
sys.exit(1 if bad else 0)
