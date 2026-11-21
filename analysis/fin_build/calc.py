import json,glob,datetime as dt
R={}
for f in glob.glob('data/raw/*.jsonl'):
    for l in open(f):
        if l.strip():
            r=json.loads(l); R[r['id']]=r
L=lambda n:R['rec:loan:%04d'%n]
F=lambda n:R['press:fact:%04d'%n]['value']
FX=253000000000/38923077
print('FX record p7',FX)
B={'mowi':range(1,7),'hendy':range(7,12),'gm':range(12,17),'tuiu':range(17,23),'franede':range(23,30),'aime':range(30,36)}
tot={'USD':0,'PYG':0}
for b,rg in B.items():
    g={'USD':0,'PYG':0};o={'USD':0,'PYG':0};od={'USD':0,'PYG':0}
    for n in rg:
        r=L(n)
        if r['principal']: g[r['currency']]+=r['principal']
        if r['outstanding']:
            o[r['currency']]+=r['outstanding']
            if r['kind']=='overdraft': od[r['currency']]+=r['outstanding']
    comb=o['USD']*6500+o['PYG']
    print(b,'granted',g,'outst',o,'od_out',od,'comb@6500',comb, 'USDeq',comb/6500,'od share',(od['USD']*6500+od['PYG'])/comb if comb else None)
    for c in o: tot[c]+=o[c]
print('six outstanding',tot, tot['USD']*6500+tot['PYG'], (tot['USD']*6500+tot['PYG'])/6500)
six=tot['USD']*6500+tot['PYG']
print('vs cap',six/F(83),'vs PE(cap*5)',six/(F(83)*5),'vs 2460',six/F(84))
print('PYG excl AIME',tot['PYG']-52364312369)
# implied fx
print('mowi fx',(254157320385-100500000000)/23266645.18)
print('hendy fx',(252521261384-99587231967)/25230739.28)
gm_usd=13567500+4321500+5326500+6305659.87
print('gm fx',(237105585238-55970014590)/gm_usd)
print('franede fx',314001127279/(25024500+10645965+15413120))
# ratios
print('hendy debt/income',252521261384/(73e6*12))
hi=99587231967*.2415; hu=5075250*.08+5527500*.075+14627989.28*.08
print('hendy interest pyg od',hi,'usd',hu,'total@6500',hi+hu*6500,(hi+hu*6500)/876e6)
print('gm exposure/income',237105585238/10576e6,'/equity',237105585238/5327e6,'LT/eq',125356/5327,'LT/inc',125356/10576,'assets',126776+5327,126776/(126776+5327))
print('gm phases usd',23100000+38923077,(23100000+38923077)*6500,(23100000+38923077)*6500/5327e6,(23100000+38923077)*6500/10576e6)
gi=13567500*.08+4321500*.08+5326500*.075
print('gm interest usd',gi,gi*6500,gi*6500/10576e6)
print('gm exposure / LT debt in statements',237105585238/125356e6)
print('franede debt/income',314001127279/(872e6*12),'granted usd',10e6+24.9e6+10.593e6+15336437.83,'pyg',160e9,'granted@6500',(10e6+24.9e6+10.593e6+15336437.83)*6500+160e9, ((10e6+24.9e6+10.593e6+15336437.83)*6500+160e9)/(872e6*12))
print('franede march income vs monthly avg',24040/872)
# 0.5% pattern
for n in [7,8,9,11,12,13,14,17,18,19,1,2,4,6,22,25,27,28,10,15,16,3,5,21,24,26,30,31,32]:
    r=L(n); print(n,r['borrower'],r['currency'],r['principal'],round(r['principal']/1.005,2), r['outstanding'] and round(r['outstanding']/r['principal'],5))
for v in [417075e6,415e9,7540000,15070000,30150000,30150e6,132660e6,100500e6,198205e6,15766440,26400000,13700000,36900e6,86100e6,93000e6,64500e6]:
    print(v, v/1.005)
# portfolio
pf={62:8,63:9,64:11,65:12,66:13,67:14,68:1,69:2,70:4}
sp=0;sf=0
for fl,ln in pf.items():
    a=R['rec:flow:%04d'%fl]['amount']; r=L(ln); p=r['principal']; d=dt.date.fromisoformat(r['date']); days=(dt.date(2026,6,15)-d).days
    acc=p*r['rate_pct']/100*days/365
    sp+=a;sf+=p
    print(fl,ln,r['borrower'],p,a,round(a/p,4),days,round(p+acc),round(a-(p+acc)), round((a/p-1)*365/days*100,2))
print('sum price',sp,'sum principal',sf,sp/sf)
# vinanzas funding
recsrc=20e6+35e6+4474670+4215767.91+10049628.97+2100000
prs=20e6+35e6+4678670+4215707+10049628+2117596
print('rec sources',recsrc,'press',prs,'diff to 76061604.13',76061604.13-recsrc,76061604.13-prs)
print('own share',93628/74418418.12,93828/74418418.12,'loans/price',81841000/74418418.12,'direct 55/price',55e6/74418418.12,'recv/loans',76061604.13/81841000)
newp=86.1e9+36.9e9+93e9+64.5e9
new=81841000*6500+newp
rem=74418418.12*6500+118244e6+109668e6+6321573.22*6500
print('new exposure',new,new/6500,'pyg loans',newp,'removed',rem,rem/6500,'net',new-rem,(new-rem)/6500)
print('related before 743784 ->', 'pct of PE', 743784/2460000, 743784e6/(F(83)*5))
# capital
for PE in [F(83)*5,2460e9,2500e9]:
    RWA=PE/0.1385
    adj=0.0556*RWA
    D1=PE-adj
    D2=(PE-0.0556*RWA)/(1-0.0556)
    Dp=1621853458972
    r1=(PE-Dp)/RWA; r2=(PE-Dp)/(RWA-Dp)
    D6=(PE-0.06*RWA)/0.94
    print('PE',PE,'RWA',RWA,'adjcap',adj,'D rwa const',D1,'D both',D2,'ratio w/ prov deficit const',r1,'both',r2,'D to hit 6%',D6, D6/(900e6*6500))
    c2=PE-Dp-876640e6; print('  after redisa/redipro',c2,c2/RWA,c2/(RWA-Dp-876640e6)); c3=c2-2105744e6; print('  after trust',c3,c3/RWA)
    print('  wipe-out loss rate on 900M', PE/(900e6*6500))
print('900M@6500',900e6*6500, 900e6*6500/F(254), 900e6*6500/F(248), 1621853458972/(900e6*6500))
print('trust/equity',F(265)/F(254),'otherinv/equity',F(264)/F(254),'trust+other assets',(F(265)+F(266))/F(254),'equity-trust',F(254)-F(265),(F(254)-F(265))/F(246))
print('facilities 5.1tn/equity24',5100e9/F(253),'/eq25',5100e9/F(254))
print('prov deficit/net result',1621853458972/F(258),'deficit/equity',1621853458972/F(254),'deficit/net loans',1621853458972/F(248))
print('redisa+redipro',F(123)+F(125),F(126),F(126)/F(254))
print('cash',17e6*6500+17e9)
# balance-sheet scenario
A=F(246);dep=F(250);soft=F(265)+F(266)+F(126)
for nm,loss in [('prov deficit',1621853458972),('Rey50',2925e9),('Rey100',5850e9)]:
    hard=A-soft-loss; print(nm,'hard',hard,hard/dep,hard/F(252))
print('soft',soft,soft/A)
# list sum
lst=[(R['press:fact:%04d'%i]['entity'],F(i)) for i in range(1,23)]
s=sum(v for e,v in lst if e!='org:ips'); print('list sum ex IPS',s,s/6500, 'incl',sum(v for e,v in lst))
grp=sum(v for e,v in lst if e not in('org:ips','org:valores-casa-de-bolsa')); print('ex IPS & Valores',grp,grp/6500)
plus=grp+six; print('plus six outstanding',plus,plus/6500, plus/(900e6*6500))
# second ring
print('gsr',453828e6/100e6,439134e6/100e6,439134/10685,439134/124448,97800/439134)
print('nubicom',228431e6/200000,85/670, 417075/1825988*1e0, 415000/1825988)
print('sagas',268363e6/84319401,'la tropa',246498e6/250e6,65e9/2238e6,'nme',198962e6/6500,198962e6/6500/33e6,198962e6/6500/5160508,33e6/5160508)
print('berilo',30.15+26.4,3.8/69)
print('hd',35e6*6500+36.9e9,'facto',6841000*6500+157.5e9,'satec',20e6*6500)
# group
print('GV val share',F(157)/F(128),1708614/2454213,'div/rev',F(158)/F(128),'assoc/assets',F(155)/F(134),'UH/assets',F(156)/F(134),'UH/equity',F(156)/F(138),'eq-UH',F(138)-F(156),'div/fin debt',F(158)/F(140),'bonds/findebt',F(162)/F(140),'nr-val',F(132)-F(157))
print('GV cash/st',71/54,'cash/debt',71/341,'bonds/debt',204/341)
print('ITTI interco/equity',F(199)/F(191),'interco growth',F(199)/F(198),'rev growth',F(179)/F(178),'gm',F(181)/F(179),'ebitda m',F(183)/F(179),'recv/revenue',F(199)/F(179),'bankdebt',F(195),'cash/st',35/22,'liab/eq',F(189)/F(191))
print('bank-financed group paper',10e6+10e6+6.841e6)
print('U stake',F(290)/202.1e6)
# dates
d=lambda s:dt.date.fromisoformat(s)
for a,b in [('2025-10-27','2026-11-02'),('2026-04-29','2026-11-02'),('2026-06-05','2026-11-02'),('2026-06-15','2026-11-02'),('2026-06-19','2026-11-02'),('2026-07-10','2026-11-02'),('2026-08-05','2026-11-02'),('2026-08-05','2026-09-24'),('2026-06-15','2026-08-05'),('2025-08-29','2026-11-02'),('2024-05-27','2026-11-02')]:
    print(a,b,(d(b)-d(a)).days)
# depositors
print('pub funds usd@6500',3600e9/6500+233.4e6,'FGD share',740/2800,928/2800,'uninsured',2800-740,2800-928,600/(2800-740),600/(2800-928),'FGD use',928/1600,740/1600)
print('IPS', 2030e9/F(250))
