import json,sys
d=json.load(open('/home/claude/work/data.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for x in d:
    if a<=x['n']<=b:
        print(f"#{x['n']} {x['q']}")
        for i,o in enumerate(x['o']): print(f"  {'ABCDEFGH'[i]}. {o if o else '(see image)'}")
        if 'qi' in x: print("  [has IAM policy image]")
