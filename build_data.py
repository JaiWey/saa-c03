import json, re, base64
d = json.load(open('bank.json'))
imgs = {
 96:  dict(q=['p270-000']),
 253: dict(q=['p702-000','p702-001']),
 423: dict(q=['p1086-000']),
 429: dict(q=['p1099-000']),
 477: dict(q=['p1197-000'], o={'A':'p1197-001','B':'p1197-002','C':'p1197-003','D':'p1197-004'}),
 494: dict(q=['p1233-000']),
}
def b64(name):
    return 'data:image/png;base64,' + base64.b64encode(open(f'img/{name}.png','rb').read()).decode()
have = {x['n'] for x in d}
# Q868 option A missing in the source
for x in d:
    if x['n'] == 868 and len(x['o']) == 3: pass
out = []
for x in d:
    m = re.match(r'([A-H]+)\s*\((\d+)%\)', x['v'] or '')
    cv, cp = (m.group(1), int(m.group(2))) if m else ('', 0)
    o = dict(n=x['n'], q=x['q'], o=x['o'], a=x['a'])
    if cv: o['cv'] = cv; o['cp'] = cp
    if x['v']: o['v'] = x['v']
    if x['n'] in imgs:
        im = imgs[x['n']]
        o['qi'] = [b64(k) for k in im['q']]
        if 'o' in im: o['oi'] = [b64(im['o'][l]) for l in 'ABCD']
    out.append(o)
out.sort(key=lambda z: z['n'])
json.dump(out, open('data.json','w'), ensure_ascii=False, separators=(',',':'))
import os; print(len(out), os.path.getsize('data.json')//1024, 'KB')
print([x['n'] for x in out if x['n']>=866 and x['n']<=870])
print([ (x['n'],x['o'],x['a']) for x in out if x['n']==868])
