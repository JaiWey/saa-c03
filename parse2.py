import re, json, sys, collections
from spellchecker import SpellChecker
sp = SpellChecker()
LIGS = ['fi','fl','ff','ffi','ffl']
FRAG = set('rst eet lter ltering lters nancial ndings ows rewall rewalls nish nishes nds ve nal nally ight ood elds exible uctuates uctuating lls rm xed ght gure gured gures guring'.split())
fixlog = collections.Counter()
inD = lambda w: w.lower() in sp
SMALL = {'t','c','x','xed','ed','er','ng','ly','s','le','les','ve','ll','nd','nds','ne','nes','nal','rm','xes'}

def fixtext(s):
    s = re.sub(r'(DynamoD|\bAL|\bNL)(?=[A-Z][a-z])', lambda m: m.group(1)+('B. ' if m.group(1)=='DynamoD' else {'AL':'ALB. ','NL':'NLB. ',}[m.group(1)]), s)
    s = re.sub(r'VPCon\s*figure','VPC. Configure',s); s = re.sub(r'\bVP(?=(?:Update|Create|Add|Use|Modify|Enable|Set)\b)','VPC. ',s)
    # manual 'le' = file
    s = re.sub(r'\ble\b(?=\s+(?:server|servers|system|systems|share|shares|gateway|storage|transfer|format|name|type|size|permissions?|access|upload|uploads|path|paths|metadata|content|contents|integrity|versions?|archive|sizes|restore|systems?s?)\b)', 'file', s)
    s = re.sub(r'\bles\b(?=\s+(?:to|from|in|on|that|are|and|or|with|by|for|into|using|as|stored|over|at|across|between|daily|can|will|must|every|each)\b)', 'files', s)
    s = re.sub(r'\bles\b', lambda m: 'files', s) if False else s
    s = s.replace('lesystem', 'filesystem')
    toks = s.split(' ')
    out = []
    i = 0
    while i < len(toks):
        t = toks[i]
        m = re.match(r'^([^A-Za-z]*)([A-Za-z]+)([^A-Za-z]*)$', t)
        if i+1 < len(toks):
            n = toks[i+1]
            m2 = re.match(r'^([^A-Za-z]*)([A-Za-z]+)([^A-Za-z]*)$', n)
            if m and m2 and not m[3] and not m2[1] and m2[2][0].islower() and not m[2].isupper() and not (m[2].lower()=='a' and inD('fi'+m2[2])):
                x, y = m[2], m2[2]
                done = False
                for lig in LIGS:
                    j = x + lig + y
                    if inD(j) and (not inD(x) or not inD(y) or y.lower() in SMALL or x.lower() in {'o','e','di','bene','speci'}) and not (inD(x) and inD(y) and len(x)>2 and len(y)>2):
                        out.append(m[1]+j+m2[3]); fixlog[f'{x} {y}->{j}']+=1
                        i += 2; done = True; break
                if done: continue
        if m and m[2] in FRAG:
            w = m[2]
            for lig in LIGS:
                for cand in (lig+w, w+lig):
                    if inD(cand):
                        t = m[1]+cand+m[3]; fixlog[f'{w}->{cand}']+=1; break
                else: continue
                break
        out.append(t); i += 1
    return ' '.join(out)

CYR = str.maketrans({'А':'A','В':'B','С':'C','Е':'E','Н':'H','а':'A','с':'C','е':'E'})
txt = open('/tmp/bank.txt', encoding='utf-8').read().replace('\f', '\n')
parts = re.split(r'^\s*Question #(\d+)\s+Topic (\d+)\s*$', txt, flags=re.M)
out = []; bad = []
for i in range(1, len(parts), 3):
    num, topic, body = int(parts[i]), int(parts[i+1]), parts[i+2]
    body = re.sub(r'^\s*AWS Certified Solutions Architect - Associate SAA-C03\s*$', '', body, flags=re.M)
    body = re.split(r'\n\s*Get IT Certi', body)[0]
    m = re.search(r'^\s*Correct Answer:\s*(.+?)\s*$', body, flags=re.M)
    if not m: bad.append((num,'noans')); continue
    head = body[:m.start()]
    ans = re.sub(r'[^A-H]', '', m.group(1).translate(CYR))
    rest = body[m.end():]
    vm = re.search(r'Community vote distribution\s*\n(.*?)(?:\n\s*\n|\n\s*\S+\s+(?:Highly Voted|Most Recent))', rest, flags=re.S)
    vote = ' '.join(vm.group(1).split()) if vm else ''
    om = list(re.finditer(r'^\s*([A-H])\.\s', head, flags=re.M))
    # keep sequential A,B,C.. only
    seq = []; exp = 'A'
    for o in om:
        if o.group(1) == exp: seq.append(o); exp = chr(ord(exp)+1)
    if len(seq) < 2 or not ans: bad.append((num,'noopts')); continue
    stem = ' '.join(head[:seq[0].start()].split())
    opts = []
    for j, o in enumerate(seq):
        end = seq[j+1].start() if j+1 < len(seq) else len(head)
        opts.append(' '.join(head[o.end():end].split()))
    def post(t):
        t = re.sub(r'\ble\b','file',t); t = re.sub(r'\bles\b','files',t)
        t = re.sub(r'VPCon\s*figure','VPC. Configure',t)
        t = re.sub(r'VPC(?=(?:Update|Create)\b)','VPC. ',t)
        return t
    stem = post(fixtext(stem)); opts = [post(fixtext(o)) for o in opts]
    stem = stem.replace('- ','- ')
    opts = [re.sub(r'(\w)- (\w)', r'\1-\2', o) for o in opts]
    out.append(dict(n=num, q=stem, o=opts, a=ans, v=vote))
json.dump(out, open('bank.json','w'), ensure_ascii=False)
print(len(out), 'ok', bad, file=sys.stderr)
print(fixlog.most_common(120), file=sys.stderr)
unk = collections.Counter()
for x in out:
    for t in [x['q']]+x['o']:
        for w in re.findall(r"[A-Za-z]+", t):
            if not inD(w) and len(w)>1: unk[w.lower()]+=1
print([w for w,c in unk.most_common(500) if len(w)<=6 or True][:260], file=sys.stderr)
