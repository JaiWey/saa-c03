import json,glob,os
d=json.load(open('data.json'))
sol={}
for f in sorted(glob.glob('sol/b*.json')):
    for r in json.load(open(f)): sol[r['n']]=r
xs={}
for f in sorted(glob.glob('sol2/b*.json')):
    for r in json.load(open(f,encoding='utf-8')): xs[r['n']]=r['x']
out=[]
diff=0
for q in d:
    s=sol[q['n']]
    mine=s['a'].replace(',','')
    o=dict(n=q['n'],q=q['q'],o=list(q['o']),a=mine,e=s['e'])
    if q['n']==868: o['o'][0]='(Option text is missing in the source PDF)'
    if q['n']==237:  # source PDF merged the question tail and option A
        o['q']=q['q']+'A. The connectivity should not have a single point of failure or bandwidth concerns. Which solution will meet these requirements?'
        o['o'][0]='Set up a VPC peering connection between VPC-A and VPC-B.'
    if q['n']==756 and len(o['o'])==2:  # source PDF merged options B, C, D into one
        import re
        parts=re.split(r'\s+(?:B|D)\.\s+',o['o'][1])
        o['o']=[o['o'][0]]+parts
    if q.get('a'): o['pa']=q['a']
    if q.get('v'): o['v']=q['v']
    if 'qi' in q: o['qi']=q['qi']
    if 'oi' in q: o['oi']=q['oi']
    if q['n'] in xs: o['x']=xs[q['n']]
    if q.get('a') and q['a']!=mine: diff+=1
    out.append(o)
json.dump(out,open('data_en.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(xs),'with per-option explanations');print(len(out),'questions; differ from PDF key:',diff, os.path.getsize('data_en.json')//1024,'KB')
t=open('template_en.html',encoding='utf-8').read()
os.makedirs('art_en',exist_ok=True); os.makedirs('dist_en',exist_ok=True)
open('art_en/index.html','w',encoding='utf-8').write(t.replace('__DATA__',''))
with open('art_en/bank.json','w',encoding='utf-8') as f:
    f.write('[\n'+',\n'.join(json.dumps(o,ensure_ascii=False,separators=(',',':')) for o in out)+'\n]')
blob=json.dumps(out,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
open('dist_en/index.html','w',encoding='utf-8').write(t.replace('__DATA__',blob))
print({k:os.path.getsize(k)//1024 for k in ['art_en/index.html','art_en/bank.json','dist_en/index.html']})
print([ (o['n'],o['a']) for o in out if o['n'] in (1,500,477)])
