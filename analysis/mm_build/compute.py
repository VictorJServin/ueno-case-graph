import json, collections
R='/home/claude/ueno-kg/data/raw/'
def L(f): return [json.loads(l) for l in open(R+f)]
# apply editor corrections (set actions)
corr=L('edit.corrections.jsonl')
def apply(rows):
    idx={r['id']:r for r in rows}
    for c in corr:
        r=idx.get(c['target_row'])
        if r is None or c['action'] not in('set','set_confidence'): continue
        f=c['field']
        if f.startswith('prov.'): r['prov'][f[5:]]=c['new']
        else: r[f]=c['new']
    return rows
rec=apply(L('rec.loans.jsonl')); pl=apply(L('press.loans.jsonl')); pf=apply(L('press.facts.jsonl'))
FX=6500
def gs(usd,pyg,fx=FX): return usd*fx+pyg
out={}
# (i) six record borrowers
six=['mowi','grupo-hendy','grupo-m','tuiu','franede','aime']
tot=collections.defaultdict(lambda: collections.defaultdict(float))
for r in rec:
    b=r['borrower'][4:]
    if b not in six: continue
    c=r['currency']
    tot[b]['grant_'+c]+=r['principal'] or 0
    tot[b]['out_'+c]+=r['outstanding'] or 0
    if r['status']=='cancelled': tot[b]['canc_'+c]+=r['principal'] or 0
    if (r['outstanding'] or 0)>0:
        tot[b]['out_'+('asf' if r['collateral'] in('none','mortgage_claimed') else 'ns')+'_'+c]+=r['outstanding']
        if r['kind']=='overdraft': tot[b]['od_'+c]+=r['outstanding']
S=collections.defaultdict(float)
for b in six:
    for k,v in tot[b].items(): S[k]+=v
    print(b,{k:round(v/1e6,2) for k,v in tot[b].items()})
print('SIX',{k:round(v/1e6,2) for k,v in S.items()})
six_out_gs=gs(S['out_USD'],S['out_PYG']); print('six outstanding Gs bn',six_out_gs/1e9,'USD M',six_out_gs/FX/1e6)
asf=gs(S['out_asf_USD'],S['out_asf_PYG']); print('explicit sole-signature share',asf/six_out_gs)
print('granted Gs bn',gs(S['grant_USD'],S['grant_PYG'])/1e9,'cancelled Gs bn',gs(S['canc_USD'],S['canc_PYG'])/1e9)
# June 15 effect: nine sold loans (term USD loans of mowi, hendy, grupo-m outstanding) + overdrafts cancelled
sold=sum(r['principal'] for r in rec if r['borrower'][4:] in('mowi','grupo-hendy','grupo-m') and r['kind']=='loan' and r['currency']=='USD' and r['status']=='outstanding')
print('sold principal',sold)
od_usd=6305659.87; od_pyg=100500000000+99587231967
six_net_usd=S['out_USD']-sold-od_usd; six_net_pyg=S['out_PYG']-od_pyg
print('six net on balance after 15 Jun: USD',six_net_usd,'PYG',six_net_pyg,'Gs bn',gs(six_net_usd,six_net_pyg)/1e9,'USD M',gs(six_net_usd,six_net_pyg)/FX/1e6)
june_repaid=gs(74418418.12+6321573.22, 118244e6+109668e6)
print('June "repayments" Gs bn',june_repaid/1e9)
tot_rep=gs(S['canc_USD'],S['canc_PYG'])+gs(sold+od_usd,od_pyg)
print('share of granted shown as repaid',tot_rep/gs(S['grant_USD'],S['grant_PYG']))
# (ii) five June borrowers
five_usd=sum(r['principal'] for r in rec if r['id'][-4:] in('0036','0037','0038','0039','0040'))
five_pyg=36.9e9+93e9+64.5e9
lst={r['entity'][4:]:r['value'] for r in pf if r['metric']=='debt_to_ueno_bank_debtor_list'}
five_list=sum(lst[k] for k in['satec','hd-invest','technoma','la-tropa-fletes','factopar'])
print('five June: USD',five_usd,'PYG',five_pyg,'Gs bn',gs(five_usd,five_pyg)/1e9,'list Gs bn',five_list/1e9)
# sameOperation de-dup across loan rows
allrows=[('rec',r) for r in rec]+[('press',r) for r in pl]
def same(a,b):
    if a['op_number'] and a['op_number']==b['op_number']: return True
    if a['date'] and a['date']==b['date'] and a['currency']==b['currency'] and a['principal'] and b['principal'] and abs(a['principal']-b['principal'])/a['principal']<0.006:
        return True
    return False
dups=0; conflicts=[]
for i,(sa,a) in enumerate(allrows):
    for sb,b in allrows[i+1:]:
        if same(a,b):
            dups+=1
            if a['borrower']!=b['borrower']: conflicts.append((a['id'],a['borrower'],b['id'],b['borrower'],a['principal']))
print('duplicate pairs',dups,'borrower conflicts',conflicts)
# (iii) second ring: one figure per borrower, preferred: debtor list; alternates noted
ring={k:lst[k] for k in['nubicom','gsr','office-design','grupo-berilo','galadriel','nuevo-mundo-entertainment','sagas','henrici','kasas-propiedades','model','grupo-vazquez','itti','redipro','discover-paraguay','muar-srl']}
extra={'la-tropa-sae':210971e6,'dobrestec':17737e6,'tsv-del-paraguay':92307e6,'infocenter':18e6*FX}
ring_list=sum(ring.values()); ring_extra=sum(extra.values())
print('ring list Gs bn',ring_list/1e9,'extra',ring_extra/1e9)
print('debtor list total excl IPS, Valores',(sum(lst.values())-lst['ips']-lst['valores-casa-de-bolsa'])/1e9)
unsec_ring=ring['gsr']+ring['nubicom']+ring['galadriel']
# questioned book totals
book_low = gs(six_net_usd,six_net_pyg)+gs(five_usd,five_pyg)+sum(ring[k] for k in['nubicom','gsr','office-design','grupo-berilo','galadriel','nuevo-mundo-entertainment','sagas','henrici'])
book_c = gs(six_net_usd,six_net_pyg)+five_list+ring_list
book_h = book_c+ring_extra
for n,v in[('low',book_low),('central',book_c),('high',book_h)]:
    print('questioned book',n,'Gs bn',round(v/1e9,1),'USD M @6500',round(v/FX/1e6,1),'@6358.5',round(v/6358.5/1e6,1),'@6585.55',round(v/6585.55/1e6,1))
print('gross incl. six at record balances (double count warning)',(six_out_gs+five_list+ring_list)/1e9)
print('explicit unsecured share of central book',(gs(six_net_usd,six_net_pyg)*asf/six_out_gs+unsec_ring)/book_c, ' six part only', asf/six_out_gs)
# Rey named firms
named=six_out_gs+ring['office-design']+ring['henrici']+ring['model']
print('Rey named firms Gs bn',named/1e9,'USD M',named/FX/1e6,'share of 900',named/FX/9e8)
# A. capital
pd=1621853458972
rwa1=pd/(0.1385-0.0556); pe1=0.1385*rwa1
rwa2=(pd-0.0556*pd)/(0.1385-0.0556); pe2=0.1385*rwa2
print('numerator-only: RWA',rwa1/1e9,'PE',pe1/1e9,'need12',(0.12*rwa1-(pe1-pd))/1e9)
print('both: RWA',rwa2/1e9,'PE',pe2/1e9,'need12',(0.12*(rwa2-pd)-(pe2-pd))/1e9)
plc=876640e6; trust=2105744e6; intang_dec=900995e6; intang_jun=825160884847
for n,d in[('sup',pd),('sup+plc',pd+plc),('sup+plc+trust',pd+plc+trust),('sup+plc+trust+intang',pd+plc+trust+intang_dec)]:
    print(n,'deduction Gs bn',round(d/1e9,1),'USD M',round(d/FX/1e6,1),'adj PE (both)',round((pe2-d)/1e9,1),'ratio',round((pe2-d)/(rwa2-d)*100,2),'need to 12% Gs bn',round((0.12*(rwa2-d)-(pe2-d))/1e9,1),'USD M',round((0.12*(rwa2-d)-(pe2-d))/FX/1e6,1))
# F waterfall on June 2026 balance
A=25641756262733; Lb=23205211051347; Eq=2436545211386
dep=5e12/0.29
print('deposits June est Gs bn',dep/1e9)
sc={'low':dict(plc=.5,credit=pd,vis=0),'central':dict(plc=1,credit=.60*book_c,vis=0),'high':dict(plc=1,credit=.90*book_h,vis=.5*2.6e12)}
res={}
for n,s in sc.items():
    adj=trust+intang_jun+s['plc']*plc+s['credit']+s['vis']
    left=A-adj; sf=Lb-left
    res[n]=dict(adj=adj,left=left,short=sf,cov_dep=left/dep,nondep_rec=max(0,(left-dep))/(Lb-dep))
    print(n,'writedown Gs bn',round(adj/1e9,1),'USD M',round(adj/FX/1e6),'left',round(left/1e9,1),'shortfall Gs bn',round(sf/1e9,1),'USD M @6500',round(sf/FX/1e6),'@6358.5',round(sf/6358.5/1e6),'@6585.55',round(sf/6585.55/1e6),'cov deposits',round(left/dep,3),'non-deposit recovery',round(res[n]['nondep_rec'],3), 'implied LGD',round(s['credit']/ (book_h if n=='high' else book_c),3))
# high-case uninsured recovery
first=(928e6+600e6)*FX
lefth=res['high']['left']; rest=dep-first
print('high: recovery for non-first-order deposits',(lefth-first)/rest)
firstc=(740e6+450e6)*FX
print('cash Rey USD M',(17e6*FX+17e9)/FX/1e6,' ABC cash Gs M',1176+881+500+480+1500)
print('public funds MEF @6500',(3.6e12/FX+233.4e6)/1e6)
json.dump(dict(S=dict(S),six_out_gs=six_out_gs,six_net_usd=six_net_usd,six_net_pyg=six_net_pyg,five_usd=five_usd,five_pyg=five_pyg,five_list=five_list,ring_list=ring_list,ring_extra=ring_extra,book_low=book_low,book_c=book_c,book_h=book_h,named=named,rwa2=rwa2,pe2=pe2,rwa1=rwa1,pe1=pe1,res=res,dep=dep,asf_share=asf/six_out_gs,sold=sold,tot_rep=tot_rep),open('/home/claude/ueno-kg/analysis/mm_build/numbers.json','w'),indent=1)
