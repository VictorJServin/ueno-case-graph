import json, shutil, os, re, glob
from rdflib import Dataset, URIRef, Graph
shutil.rmtree('pub',ignore_errors=True); shutil.copytree('site','pub')
os.remove('pub/TESTLOG.md') if os.path.exists('pub/TESTLOG.md') else None
ren={'graph.jsonld':'graph.json','graph.ttl':'graph.ttl.txt','graph.trig':'graph.trig.txt','ontology.ttl':'ontology.ttl.txt'}
for a,b in ren.items(): os.rename('pub/data/'+a,'pub/data/'+b)
for f in glob.glob('pub/js/*.js')+['pub/index.html']:
    s=open(f,encoding='utf-8').read()
    s=re.sub(r'graph\.jsonld','graph.json',s); s=re.sub(r'graph\.ttl','graph.ttl.txt',s); s=re.sub(r'graph\.trig','graph.trig.txt',s); s=re.sub(r'ontology\.ttl','ontology.ttl.txt',s)
    open(f,'w',encoding='utf-8').write(s)
# privacy: drop private individuals flagged by the editor from the public copy
names=['juan-carlos-lopez-moreira','graciela-celia-de-lopez-moreira','maria-del-mar-lopez-moreira']
p='pub/data/graph.json'; d=json.load(open(p))
drop={n['@id'] for n in d['@graph'] if any(x in json.dumps(n) for x in names)}
d['@graph']=[n for n in d['@graph'] if n['@id'] not in drop]
json.dump(d,open(p,'w'),ensure_ascii=False,separators=(',',':'))
base='https://w3id.org/ueno-case/id/'; iris={URIRef(base+i.split(':',1)[1]) for i in drop}
ds=Dataset(); ds.parse('pub/data/graph.trig.txt',format='trig')
for q in list(ds.quads((None,None,None,None))):
    if q[0] in iris or q[2] in iris: ds.remove(q)
ds.serialize('pub/data/graph.trig.txt',format='trig')
g=Graph(); g.parse('pub/data/graph.ttl.txt',format='turtle')
for t in list(g):
    if t[0] in iris or t[2] in iris: g.remove(t)
g.serialize('pub/data/graph.ttl.txt',format='turtle')
left=[f for f in glob.glob('pub/**/*',recursive=True) if os.path.isfile(f) and re.search('lopez-moreira|Lopez Moreira|López Moreira',open(f,errors='ignore').read())]
print('dropped',len(drop),'still mentioning:',left)
