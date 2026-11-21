import json, collections, datetime as dt, networkx as nx, calendar
from metrics import *
ALT|={'press:flow:0005'}; AGG|={'rec:flow:0076'}
ONLY_TO={'press:flow:0068','press:flow:0008','press:flow:0024'}  # counted for receiver only (agent leg / joint senders)
amt=[r for r in flows if r['amount'] is not None and r['id'] not in NONCASH|AGG|ALT]
clusters=[]
for r in sorted(amt,key=lambda r:(0 if r['id'].startswith('rec') else 1, r['id'])):
    for c in clusters:
        if same(c[0],r): c.append(r); break
    else: clusters.append([r])
legs=[(rep(c),[x['id'] for x in c]) for c in clusters]
ent=collections.defaultdict(collections.Counter); cps=collections.defaultdict(set); ra=collections.Counter(); rn=collections.Counter()
for r in flows:
    for e,o in ((r['from'],r['to']),(r['to'],r['from'])):
        cps[e].add(o); (ra if r['amount'] is not None else rn)[e]+=1
for r,ids in legs:
    if not (set(ids)&ONLY_TO): ent[r['from']]['out_'+r['currency']]+=r['amount']
    ent[r['to']]['in_'+r['currency']]+=r['amount']
H={}
for e in cps:
    c=ent[e]; H[e]=dict(in_usd=round(c['in_USD'],2),out_usd=round(c['out_USD'],2),in_pyg=round(c['in_PYG']),out_pyg=round(c['out_PYG']),counterparties=len(cps[e]),rows_with_amount=ra[e],rows_without_amount=rn[e])
json.dump(H,open('hubs.json','w'),indent=1)
json.dump([dict(rep=r['id'],ids=ids,frm=r['from'],to=r['to'],amount=r['amount'],currency=r['currency'],date=r['date']) for r,ids in legs],open('legs.json','w'),indent=1)
for e in ['org:vinanzas','org:itti','org:ueno-bank','org:grupo-vazquez','org:redisa','org:redipro','org:kasas-propiedades','org:la-tropa-fletes','org:factopar','org:ueno-casa-de-bolsa','org:mowi','org:grupo-hendy','org:grupo-m','org:kaitel','org:model','org:technoma']: print(e,H[e])
print('unique legs',len(legs))
# shares
five={'org:itti','org:redisa','org:redipro','org:vinanzas','org:grupo-vazquez'}
borrowers={l['borrower'] for l in loans}
fw=[(r,ids) for r,ids in legs if r['from'] in borrowers and r['instrument'] in('transfer','bond_purchase','contract') and r['to'] not in ('org:ueno-bank',) and r['from'] not in five and not (set(ids)&{'press:flow:0068'})]
tot=collections.Counter(); hit=collections.Counter(); by=collections.defaultdict(collections.Counter)
for r,ids in fw:
    tot[r['currency']]+=r['amount']
    if r['to'] in five: hit[r['currency']]+=r['amount']; by[r['currency']][r['to']]+=r['amount']
    else: by[r['currency']]['OTHER:'+r['to']]+=r['amount']
for c in tot: print('first-hop',c,'traced',tot[c],'to five',hit[c],round(100*hit[c]/tot[c],1),dict(by[c]))
# edge-count share incl null
allfw=[r for r in flows if r['from'] in borrowers and r['from'] not in five and r['instrument'] in('transfer','bond_purchase','contract','cheque') and r['to']!='org:ueno-bank']
pairs={(r['from'],r['to']) for r in allfw}
print('fwd rows',len(allfw),'to five',sum(1 for r in allfw if r['to'] in five),'; distinct pairs',len(pairs),'to five',sum(1 for p in pairs if p[1] in five))
print(collections.Counter(r['to'] for r in allfw).most_common())
# record six borrowers: disbursed totals
six=['org:mowi','org:grupo-hendy','org:grupo-m','org:tuiu','org:franede','org:aime']
for b in six:
    t=collections.Counter(); o=collections.Counter()
    for l in L('rec.loans.jsonl'):
        if l['borrower']==b and l['principal']: t[l['currency']]+=l['principal']; o[l['currency']]+=(l['outstanding'] or 0)
    tr=collections.Counter()
    for r,ids in legs:
        if r['from']==b and r['instrument']!='repayment': tr[r['currency']]+=r['amount']
    print(b,'principal',dict(t),'outstanding',dict(o),'amount-traced first hop',dict(tr))
# month-end clustering of record loans
rl=L('rec.loans.jsonl'); n=0; me=0
for l in rl:
    d=dt.date.fromisoformat(l['date']); n+=1
    last=calendar.monthrange(d.year,d.month)[1]
    if last-d.day<=5 or d.day<=4: me+=1
print('rec loans dated in last 6 days or first 4 days of month:',me,'of',n)
print(sorted(collections.Counter(l['date'] for l in rl).items()))
# explicit cycles via ueno-bank
G=nx.DiGraph()
for r in flows:
    if r['id'] in NONCASH|AGG|{'rec:flow:0074','rec:flow:0073'}: continue
    if r['instrument']=='cash_delivery': continue
    G.add_edge(r['from'],r['to'])
cyc=[c for c in nx.simple_cycles(G,length_bound=7) if 'org:ueno-bank' in c]
print('explicit simple cycles through ueno-bank (<=7 nodes):',len(cyc))
S=collections.Counter(len(c) for c in cyc); print(S)
for c in sorted(cyc,key=len)[:12]:
    i=c.index('org:ueno-bank'); print('  ',' > '.join(x.split(':')[1] for x in c[i:]+c[:i]))
