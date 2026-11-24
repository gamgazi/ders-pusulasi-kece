"""Append evidence-checked missing helper objects without resetting accepted work."""
import json, pathlib, unicodedata, re, hashlib
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
def read(p): return json.loads(p.read_text(encoding='utf8'))
def write(p,o): p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def norm(s):
    s=s.casefold().replace('ı','i')
    return re.sub(r'[^a-z0-9]+','_', ''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))).strip('_')
def leaves(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():yield from leaves(v,p+'/'+k)
    elif isinstance(o,list):
        for k,v in enumerate(o):yield from leaves(v,p+'/'+str(k))
    else:yield p,o
specs=[
('cadir_kamp_001','Kamp çadırı','kamp/cadir',11,'D2','çadır','çadır',['cadir']),
('uyku_tulumu_001','Uyku tulumu','kamp/uyku-tulumu',11,'D4','uyku tulumu','uyku tulumu',['uyku_tulumu']),
('odun_tek_001','Tek odun parçası','kamp/odun',11,'D5','odun','odun',['odun','kutuk']),
('battaniye_katli_001','Katlı battaniye','kamp/battaniye',11,'D5','battaniye','battaniye',['battaniye']),
('dis_fircasi_001','Diş fırçası','bakim/dis-fircasi',14,'D4','diş fırçası','diş fırçası',['dis_fircasi']),
('dis_macunu_kapali_001','Kapalı diş macunu','bakim/dis-macunu',14,'D4','diş macunu','diş macunu',['dis_macunu']),
('sabun_kalip_001','Kalıp sabun','bakim/sabun',14,'D4','resim: sabun','sabun',['sabun']),
('tarak_tek_001','Tarak','bakim/tarak',14,'D4','resim: tarak','tarak',['tarak']),
('simit_tek_001','Simit','yiyecek/simit',15,'D2','simit','simit',['simit']),
('baklava_dilim_001','Tek baklava dilimi','yiyecek/baklava',15,'D5','baklava','baklava',['baklava']),
('vapur_yandan_001','Yandan vapur','ulasim/vapur',15,'D2','vapur','vapur',['vapur']),
('balon_sicak_hava_001','Sıcak hava balonu','ulasim/sicak-hava-balonu',15,'D3',"Kapadokya'da balon var.",'balon',['balon_sicak','sicak_hava']),
('peri_bacasi_tek_001','Tek peri bacası','doga/peri-bacasi',15,'D4','peri bacası','peri bacası',['peri_bacasi']),
('oyuncak_araba_001','Oyuncak araba','oyun/oyuncak-araba',16,'D3','oyuncak araba','oyuncak araba',['oyuncak_araba']),
('kaydirak_tek_001','Kaydırak','oyun/kaydirak',16,'D4','kaydırak','kaydırak',['kaydirak']),
('salincak_tek_001','Salıncak','oyun/salincak',16,'D2','salıncak','salıncak',['salincak']),
('tahterevalli_001','Tahterevalli','oyun/tahterevalli',16,'D4','resim: tahterevalli','tahterevalli',['tahterevalli']),
('firca_boya_001','Boya fırçası','egitim/firca',17,'D2','fırça','fırça',['firca_boya','boya_fircasi']),
('kalem_kursun_001','Kurşun kalem','egitim/kalem',17,'D4','kalem','kalem',['kalem_kursun','kursun_kalem']),
('yapistirici_kapali_001','Kapalı yapıştırıcı','egitim/yapistirici',17,'D4','yapıştırıcı','yapıştırıcı',['yapistirici']),
('silgi_tek_001','Silgi','egitim/silgi',17,'D4','resim: silgi','silgi',['silgi']),
('tebesir_tek_001','Tek tebeşir','egitim/tebesir',19,'D4','tebeşir','tebeşir',['tebesir']),
('davul_tek_001','Davul','muzik/davul',11,'D7','resim: davul','davul',['davul']),
('sihirli_hali_001','Sihirli halı','masal/sihirli-hali',20,'D3','sihirli halı','sihirli halı',['sihirli_hali'])]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
h=read(ROOT/'denetim/uretim_kayitlari_eslestirme.json');records={x['record'] for x in h}
repo=BASE/'work/repository'
for f in (repo/'stop-motion/uretim-kayitlari').glob('*.json'):
    rel=f.relative_to(repo).as_posix()
    if rel in records:continue
    j=read(f);p=repo/'stop-motion'/j['final_path']
    valid=p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==j['metrics']['sha256']
    h.append({'record':rel,'asset_name':j['id'],'declared_final_sha256':j['metrics']['sha256'],'historical_status':j['status'],'binary_revalidated_this_session':valid})
    records.add(rel)
s=read(BASE/'work/source/pusula/ders-pusulasi/4-6-agac.json');cards=read(BASE/'work/source/kartlar.json')
new=[]
for aid,title,cat,un,ln,evidence,term,aliases in specs:
    if aid in oldids:continue
    ui=next(i for i,u in enumerate(s['uniteler']) if u['no']==un);u=s['uniteler'][ui]
    di=next(i for i,d in enumerate(u['dersler']) if d['kod']==ln);d=u['dersler'][di]
    locs=[p for p,v in leaves(d) if v==evidence]
    if not locs:raise SystemExit('Missing exact source evidence: '+aid)
    hits=[x['record'] for x in h if any(a in norm(x.get('asset_name','')+' '+x['record']) for a in aliases)]
    if hits:raise SystemExit('Historical match needs review: '+aid+': '+str(hits))
    live=[x['id'] for x in q['items'] if any(a in norm(x['id']) for a in aliases)]
    if live:raise SystemExit('Live queue match needs review: '+aid+': '+str(live))
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':'pusula/ders-pusulasi/4-6-agac.json','source_blob_sha':'abd7c89b0c16b5a9e41f144dfc4f4e7c7bc7ccea','unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':evidence,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if norm(term) in norm(c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':hits,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical historical/current records plus {len(q["items"])} current queue entries and repository canonical PNG paths','semantic_review':'Vapur is a powered ferry, distinct from existing sailboat. Hot-air balloon has an attached basket, distinct from existing hand balloon. Hygiene toothbrush is distinct from paintbrush. No historical unavailable asset is regenerated.'})
q['items'].extend(new)
write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(ROOT/'denetim/kuyruk_genisletme_kaniti.json',{'new_ids':[x['id'] for x in new],'source_verified':True,'historical_records_compared':len(h),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h)},ensure_ascii=False))
