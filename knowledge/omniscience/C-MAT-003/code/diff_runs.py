import json,sys
mod=sys.argv[1]
def flat(d,p=""):
    if isinstance(d,dict):
        for k,v in d.items(): yield from flat(v,p+"/"+k)
    elif isinstance(d,list):
        for i,v in enumerate(d): yield from flat(v,p+f"[{i}]")
    else: yield p,d
for m in ["Si","MgO","NaCl","LiF","NaF","KCl","KBr","CaO","CaF2","Al2O3","BeO"]:
    try: a=dict(flat(json.load(open(f"out/run1/{mod}/{m}.json")))); b=dict(flat(json.load(open(f"out/run2/{mod}/{m}.json"))))
    except FileNotFoundError: continue
    worst={}
    for k in a:
        x,y=a[k],b.get(k)
        if isinstance(x,float) and isinstance(y,float) and x!=y:
            g=k.split("[")[0]; r=abs(x-y)/max(abs(x),1e-9); worst[g]=max(worst.get(g,0),r)
        elif x!=y: worst[k]="neq"
    print(mod,m,{k:(f"{v:.1e}" if isinstance(v,float) else v) for k,v in worst.items() if "fmin" not in k})
