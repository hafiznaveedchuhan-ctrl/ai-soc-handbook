import sys, re
from html.parser import HTMLParser
class P(HTMLParser):
    SKIP={'script','style','nav','header','footer','svg','noscript','button','form'}
    BLOCK={'p','div','li','tr','h1','h2','h3','h4','h5','h6','br','table','section','article','dt','dd','pre','td','th'}
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in s.SKIP: s.skip+=1
        if t in s.BLOCK: s.out.append('\n')
        if t in ('td','th'): s.out.append(' | ')
    def handle_endtag(s,t):
        if t in s.SKIP and s.skip: s.skip-=1
        if t in s.BLOCK: s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='replace').read())
t=re.sub(r'[ \t]+',' ',''.join(p.out)); t=re.sub(r'\n\s*\n+','\n\n',t)
open(sys.argv[2],'w').write(t.strip()+'\n')
