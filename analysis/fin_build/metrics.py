import json, collections, itertools, datetime as dt, sys
R='/home/claude/ueno-kg/data/raw/'
def L(f): return [json.loads(l) for l in open(R+f,encoding='utf-8') if l.strip()]
flows=L('rec.flows.jsonl')+L('press.flows.jsonl')
loans=L('rec.loans.jsonl')+L('press.loans.jsonl')
# ---- coverage
def cov(rows):
    a=sum(1 for r in rows if r['amount'] is not None); return a,len(rows)-a
cv={'rec':cov([r for r in flows if r['id'].startswith('rec')]),'press':cov([r for r in flows if r['id'].startswith('press')]),'all':cov(flows)}
# ---- exclusions from money totals
NONCASH={r['id'] for r in flows if r['instrument']=='portfolio_assignment'}
AGG={'rec:flow:0075'}                      # Rey aggregate with stand-in recipient
ALT={'press:flow:0006','press:flow:0007'}  # same money printed as ITTI->Vinanzas (press:flow:0053/0054)
# ---- dedup of repeated reports of one leg
def ym(d): return (d or '')[:7]
def same(a,b):
    if (a['from'],a['to'],a['currency'])!=(b['from'],b['to'],b['currency']): return False
    x,y=a['amount'],b['amount']
    if abs(x-y)/max(x,y)>0.05: return False
    da,db=a['date'] or '',b['date'] or ''
    if not da or not db: return True
    if len(da)>=7 and len(db)>=7: 
        if ym(da)!=ym(db): return False
        if len(da)==10 and len(db)==10 and da!=db: return abs((dt.date.fromisoformat(da)-dt.date.fromisoformat(db)).days)<=4
        return True
    return da[:4]==db[:4]
amt=[r for r in flows if r['amount'] is not None and r['id'] not in NONCASH|AGG|ALT]
clusters=[]
for r in sorted(amt,key=lambda r:(0 if r['id'].startswith('rec') else 1, r['id'])):
    for c in clusters:
        if same(c[0],r): c.append(r); break
    else: clusters.append([r])
def rep(c):
    # representative: press exact (non-approx, medium) beats rec diagram 'low'; else rec; else first non-approx
    best=None
    for r in c:
        score=(r['prov']['confidence']!='low', not r.get('amount_is_approx'), len(r['date'] or ''), r['id'].startswith('rec'), (r['amount']*100)%100!=0)
        if best is None or score>best[0]: best=(score,r)
    return best[1]
legs=[(rep(c),[x['id'] for x in c]) for c in clusters]
if __name__=='__main__':
    print('coverage (with amount, null):',cv)
    print('amount rows used',len(amt),'-> unique legs',len(legs))
    for r,ids in legs:
        if len(ids)>1: print('  merged',r['from'][4:],'>',r['to'][4:],r['amount'],r['currency'],r['date'],'rep',r['id'],ids)
    ent=collections.defaultdict(lambda: collections.Counter())
    cps=collections.defaultdict(set); rows_amt=collections.Counter(); rows_null=collections.Counter()
    for r in flows:
        for e,o in ((r['from'],r['to']),(r['to'],r['from'])):
            cps[e].add(o)
            (rows_amt if r['amount'] is not None else rows_null)[e]+=1
    for r,ids in legs:
        ent[r['from']]['out_'+r['currency']]+=r['amount']; ent[r['to']]['in_'+r['currency']]+=r['amount']
    out={}
    for e in sorted(cps,key=lambda e:-(rows_amt[e]+rows_null[e])):
        c=ent[e]
        out[e]=dict(in_usd=round(c['in_USD'],2),out_usd=round(c['out_USD'],2),in_pyg=round(c['in_PYG']),out_pyg=round(c['out_PYG']),counterparties=len(cps[e]),rows_with_amount=rows_amt[e],rows_without_amount=rows_null[e])
        print(e, out[e])
    json.dump(out,open('/home/claude/ueno-kg/analysis/fin_build/hubs_raw.json','w'),indent=1)
    # pass-through: in and out dated within 0-4 days (day precision), all rows incl. null amounts
    def d(r):
        try: return dt.date.fromisoformat(r['date']) if r['date'] and len(r['date'])==10 else None
        except: return None
    pt=collections.Counter(); ptd=collections.defaultdict(set)
    for e in cps:
        ins=[r for r in flows if r['to']==e and d(r) and r['id'] not in NONCASH]; outs=[r for r in flows if r['from']==e and d(r) and r['id'] not in NONCASH]
        for i in ins:
            for o in outs:
                g=(d(o)-d(i)).days
                if 0<=g<=4: ptd[e].add((i['date'],o['date']))
        pt[e]=len(ptd[e])
    print('pass-through date pairs (in->out within 0-4 days):')
    for e,n in pt.most_common(14): print(' ',e,n,sorted({a for a,b in ptd[e]}))
    # dated-day share
    print('rows with day-precision date:',sum(1 for r in flows if d(r)),'of',len(flows))
