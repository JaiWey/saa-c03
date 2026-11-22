import json,sys
d={q['n']:q for q in json.load(open('data_en.json',encoding='utf-8'))}
b=json.load(open(f'sol/b{int(sys.argv[1]):03d}.json',encoding='utf-8'))
x={r['n']:r['x'] for r in json.load(open(f'sol2/b{int(sys.argv[1]):03d}.json',encoding='utf-8'))}
bad=[]
for r in b:
    q=d[r['n']];L=set('ABCDEFGH'[:len(q['o'])])
    if r['n'] not in x or set(x[r['n']])!=L: bad.append(r['n'])
print('missing/mismatch:',bad, 'count',len(x))
