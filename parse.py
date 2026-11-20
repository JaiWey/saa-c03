import re, json, sys
txt = open('/tmp/bank.txt', encoding='utf-8').read()
txt = txt.replace('\f', '\n')
# split by question header
parts = re.split(r'^\s*Question #(\d+)\s+Topic (\d+)\s*$', txt, flags=re.M)
qs = []
for i in range(1, len(parts), 3):
    num, topic, body = int(parts[i]), int(parts[i+1]), parts[i+2]
    qs.append((num, topic, body))
print(len(qs), file=sys.stderr)
out = []
bad = []
for num, topic, body in qs:
    # strip page header lines
    body = re.sub(r'^\s*AWS Certified Solutions Architect - Associate SAA-C03\s*$', '', body, flags=re.M)
    m = re.search(r'^\s*Correct Answer:\s*([A-Z ,]+?)\s*$', body, flags=re.M)
    if not m:
        bad.append((num, 'noanswer')); 
        continue
    head = body[:m.start()]
    ans = re.sub(r'[^A-Z]', '', m.group(1))
    rest = body[m.end():]
    # community vote
    vm = re.search(r'Community vote distribution\s*\n(.*?)(?:\n\s*\n|\n\s*\S+\s+(?:Highly Voted|Most Recent))', rest, flags=re.S)
    vote = ''
    if vm:
        vote = ' '.join(vm.group(1).split())
    # options
    om = list(re.finditer(r'^\s{0,6}([A-H])\.\s', head, flags=re.M))
    if len(om) < 2:
        bad.append((num, 'noopts')); continue
    stem = head[:om[0].start()]
    opts = []
    for j, o in enumerate(om):
        end = om[j+1].start() if j+1 < len(om) else len(head)
        t = ' '.join(head[o.end():end].split())
        opts.append(t)
    stem = '\n'.join(l.rstrip() for l in stem.strip().split('\n'))
    stem = re.sub(r'\n{2,}', '\n', stem)
    # join wrapped lines: keep paragraph-ish; simple: join lines with space except keep final question line
    stem = ' '.join(stem.split())
    out.append(dict(n=num, topic=topic, q=stem, o=opts, a=ans, v=vote))
json.dump(out, open('bank.json','w'), ensure_ascii=False)
print(len(out), 'ok', len(bad), 'bad', bad[:20], file=sys.stderr)
