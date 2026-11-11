"""Write <page>.flashcards.yaml and <page>.quiz.yaml from compact data.
Correct option is given first in data; it is moved to a rotating position so answers spread
(pattern below: no run > 3, no position > 60%)."""
import json
PAT=[1,3,0,2,1,0,3,2]
def q(s): return json.dumps(s, ensure_ascii=False)
def write(path_base, title, cards, questions):
    out=["deck:",f"  title: {q(title)}",f"  description: {q('Recall checks drawn only from the page '+title+'.')}","cards:"]
    for f,b in cards: out+= [f"  - front: {q(f)}",f"    back: {q(b)}"]
    open(path_base+".flashcards.yaml","w").write("\n".join(out)+"\n")
    out=["quiz:",f"  title: {q(title)}",f"  questionsPerRound: {len(questions)}","questions:"]
    for i,t in enumerate(questions):
        stem,right,wrong,expl,src=t[0],t[1],list(t[2:-2]),t[-2],t[-1]
        pos=PAT[i%len(PAT)]%(len(wrong)+1); opts=list(wrong); opts.insert(pos,right)
        out+=[f"  - question: {q(stem)}","    options:"]+[f"      - {q(o)}" for o in opts]
        out+=[f"    answer: {pos}",f"    explanation: {q(expl)}",f"    source: {q(src)}"]
    open(path_base+".quiz.yaml","w").write("\n".join(out)+"\n")
