from metrics import *
import datetime as dt
rl={l['id']:l for l in L('rec.loans.jsonl')}
print('--- 1.005 test')
for l in loans:
    p=l['principal']
    if not p: continue
    b=p/1.005
    unit=1e6 if l['currency']=='PYG' else 50
    ok=abs(b/unit-round(b/unit))<1e-6
    rnd=abs(p/unit - round(p/unit))<1e-6 and (p % (1e9 if l['currency']=='PYG' else 1e5)==0)
    o=l.get('outstanding')
    print(l['id'],l['borrower'][4:],l['date'],l['currency'],p,'base',round(b,2),'x1.005' if ok else '', 'round' if rnd else '', 'out/prin=%.5f'%(o/p) if o else '')
print('--- portfolio price vs principal')
items=[('rec:flow:%04d'%i) for i in range(62,71)]
F={r['id']:r for r in flows}
tp=tq=0
for i in items:
    f=F[i]; l=rl[f['linked_loan']]; d=(dt.date(2026,6,15)-dt.date.fromisoformat(l['date'])).days
    acc=l['principal']*(1+l['rate_pct']/100*d/365); acc2=l['principal']*1.005*(1+l['rate_pct']/100*d/365)
    print(i,l['borrower'][4:],l['op_number'],l['principal'],f['amount'],round(f['amount']/l['principal'],5),'days',d,'par+int365',round(acc),'x1.005',round(acc2))
    tp+=l['principal']; tq+=f['amount']
print('sum principal',tp,'sum price',tq,tq/tp, 74418418.12-tp)
print('--- circuit arithmetic')
rec=[20000000,35000000,4474670,4215767.91,10049628.97,2100000]; print('record legs sum',sum(rec),'gap',76061604.13-sum(rec))
pr=[20000000,35000000,10049628.97,4678670.99,2117596.26]; print('GV implied',76061604.13-sum(pr))
pr5=[20000000,35000000,10049628,4215707,2117596,4678670]; print('UH5Nov sum',sum(pr5),76061604.13-sum(pr5))
pr10=[20e6,35e6,10.04e6,4.67e6,4.21e6,2.11e6]; print('UH10Nov rounded sum',sum(pr10))
print('residual',76061604.13-74418418.12,'with opening',76061604.13+93828-74418418.12, 76061604.13+93628-74418418.12)
print('ITTI in',4230383.21+5769861,'out',6321574+4678670.99,'short',6321574+4678670.99-(4230383.21+5769861))
print('uses vs loans',76061604.13+6321574-81841000)
print('LaTropa rest',9923899.99-4215707.91-2117596.26,'Factopar other >=0 => x>=',10049628.97-6841000, 'y<=',9923899.99-4215707.91-2117596.26-(10049628.97-6841000))
print('PYG: lines 218700 -sagas-hd =',218700-86100-36900,'factopar pyg loans',93000+64500,'vin in',218700+31200,'vin out',110940+18770,'overdrafts',118244+109668,'redisa out',110940+98202)
print('rates: nubicom',285.6e9/33e6,'office',96767e6/15.6e6,'latropa',36172717196/5936654.88)
print('mowi',33.5e9/5366645.18,'hendy',91334400000/14627989.28,'franede95',95e9/15336437.83,'franede65',65e9/10593000, 'days',(dt.date(2026,3,27)-dt.date(2025,6,30)).days, 1+0.08*270/365, 1+.08*270/360)
