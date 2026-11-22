import json,sys
d={q['n']:q for q in json.load(open('data_en.json',encoding='utf-8'))}
b=json.load(open(f'sol/b{int(sys.argv[1]):03d}.json',encoding='utf-8'))
for r in b:
    q=d[r['n']]
    print(f"#{r['n']} [{r['a'].replace(',','')}] {q['q']}")
    for i,o in enumerate(q['o']): print(f"  {'ABCDEFGH'[i]}. {o or '(image)'}")
    pass
