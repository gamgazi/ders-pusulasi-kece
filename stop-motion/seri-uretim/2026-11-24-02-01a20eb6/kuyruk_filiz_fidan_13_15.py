"""Append verified 13-15 Filiz and Fidan object queue after record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE=None
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def norm(s):return re.sub('[^a-z0-9]+','_', ''.join(c for c in unicodedata.normalize('NFKD',s.casefold().replace('ı','i')) if not unicodedata.combining(c))).strip('_')
def matches(a,s):return ('_'+a+'_') in ('_'+norm(s)+'_')
def leaves(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():yield from leaves(v,p+'/'+k)
    elif isinstance(o,list):
        for k,v in enumerate(o):yield from leaves(v,p+'/'+str(k))
    else:yield p,o
specs=[
  [
    "kulaklik_tek_001",
    "Tek baş bantlı kulaklık",
    "teknoloji/kulaklik",
    "13-15-filiz",
    12,
    "D6",
    "kulaklık",
    [
      "kulaklik"
    ]
  ],
  [
    "levha_yon_tek_001",
    "Tek yön levhası",
    "ulasim/yon-levhasi",
    "13-15-filiz",
    6,
    "D2",
    "levha",
    [
      "levha_yon",
      "yon_levhasi"
    ]
  ],
  [
    "recete_ornek_001",
    "Tek boş örnek reçete",
    "kirtasiye/recete",
    "13-15-filiz",
    7,
    "D3",
    "reçete",
    [
      "recete"
    ]
  ],
  [
    "hamur_tek_001",
    "Tek yoğrulmuş yemek hamuru",
    "yiyecek/hamur",
    "13-15-filiz",
    14,
    "D2",
    "hamur",
    [
      "hamur_tek",
      "yemek_hamuru"
    ]
  ],
  [
    "nohut_tek_001",
    "Tek nohut tanesi",
    "yiyecek/nohut",
    "13-15-filiz",
    14,
    "D6",
    "nohut",
    [
      "nohut"
    ]
  ],
  [
    "tereyagi_kalip_001",
    "Tek tereyağı kalıbı",
    "yiyecek/tereyagi",
    "13-15-filiz",
    14,
    "D6",
    "Kurabiyeyi un, şeker ve tereyağından yaparız.",
    [
      "tereyagi"
    ]
  ],
  [
    "seker_paketi_kapali_001",
    "Tek kapalı toz şeker paketi",
    "yiyecek/seker-paketi",
    "13-15-filiz",
    14,
    "D6",
    "Kurabiyeyi un, şeker ve tereyağından yaparız.",
    [
      "seker_paketi",
      "toz_seker"
    ]
  ],
  [
    "firin_kapali_001",
    "Tek kapalı mutfak fırını",
    "mutfak/firin",
    "13-15-fidan",
    3,
    "D4",
    "fırını ısıtmak",
    [
      "firin_kapali",
      "mutfak_firini"
    ]
  ],
  [
    "kek_kalibi_bos_001",
    "Tek boş halka kek kalıbı",
    "mutfak/kek-kalibi",
    "13-15-fidan",
    3,
    "D4",
    "kalıbı yağlamak",
    [
      "kek_kalibi"
    ]
  ],
  [
    "cirpici_tek_001",
    "Tek el çırpıcısı",
    "mutfak/cirpici",
    "13-15-fidan",
    3,
    "D4",
    "çırpmak",
    [
      "cirpici"
    ]
  ],
  [
    "ic_lastik_sonuk_001",
    "Tek sönük bisiklet iç lastiği",
    "ulasim/ic-lastik",
    "13-15-fidan",
    3,
    "D6",
    "Tekerleği çıkardıktan sonra iç lastiğe bak.",
    [
      "ic_lastik"
    ]
  ],
  [
    "yama_lastik_tek_001",
    "Tek lastik yama parçası",
    "ulasim/lastik-yamasi",
    "13-15-fidan",
    3,
    "D6",
    "yama yapmak",
    [
      "yama_lastik",
      "lastik_yamasi"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/filiz_fidan_13_15_kuyruk_kaniti.json'
if all(s[0] in oldids for s in specs):
    print(json.dumps({'already_appended':True,'proof_preserved':proof.exists()}));raise SystemExit(0)
cards=read(BASE/'work/source/kartlar.json')
sources={}
for tag in {s[3] for s in specs}:
    path='pusula/ders-pusulasi/'+tag+'.json'
    raw=(BASE/'work/source'/path).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    expected=subprocess.check_output(['git','rev-parse','HEAD:'+path],cwd=REPO,text=True).strip()
    assert blob==expected, 'Source Git blob mismatch'
    sources[tag]=(path,blob,json.loads(raw))
h=read(ROOT/'denetim/uretim_kayitlari_eslestirme.json');records={x['record'] for x in h}
for f in (REPO/'stop-motion/uretim-kayitlari').glob('*.json'):
    rel=f.relative_to(REPO).as_posix()
    if rel in records:continue
    j=read(f);p=REPO/'stop-motion'/j['final_path']
    valid=p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==j['metrics']['sha256']
    assert valid,'Canonical binary missing or changed: '+rel
    h.append({'record':rel,'asset_name':j['id'],'declared_final_sha256':j['metrics']['sha256'],'historical_status':j['status'],'binary_revalidated_this_session':valid});records.add(rel)
canonical=[p.relative_to(REPO).as_posix() for p in (REPO/'stop-motion').rglob('*.png') if 'seri-uretim' not in p.parts]
new=[]
for aid,title,cat,tag,un,ln,term,aliases in specs:
    SOURCE,blob,source=sources[tag]
    if aid in oldids:continue
    ui=next(i for i,u in enumerate(source['uniteler']) if u['no']==un);u=source['uniteler'][ui]
    di=next(i for i,d in enumerate(u['dersler']) if d['kod']==ln);d=u['dersler'][di]
    locs=[p for p,v in leaves(d) if v==term];assert locs,aid+' missing source evidence'
    historical=[x['record'] for x in h if any(matches(a,x.get('asset_name','')+' '+x['record']) for a in aliases)]
    existing=[x['id'] for x in q['items']+new if any(matches(a,x['id']) for a in aliases)]
    files=[x for x in canonical if any(matches(a,x) for a in aliases)]
    assert not historical and not existing and not files, (aid,historical,existing,files)
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':aid in {'tereyagi_kalip_001','seker_paketi_kapali_001','firin_kapali_001','kek_kalibi_bos_001','cirpici_tek_001','ic_lastik_sonuk_001','yama_lastik_tek_001'},'semantic_review':"13–15 Filiz ve Fidan derslerinin seçilen tam bağlamları okundu. Baş bantlı kulaklık tek bağlı nesnedir; iki ayrı kulak içi kulaklık üretilmez. Yön levhasında genel ok ve PARK yazısı tasarım kararıdır; resmi trafik işareti ölçüsü/standardı iddiası yoktur. Reçete yalnız boş ÖRNEK sahne kâğıdıdır; ilaç adı, doz, hasta veya hekim bilgisi içermez. Yemek hamuru tek yoğrulmuş kütledir; oyun hamuru kabı ve ince yufka değildir. Tek nohut tanesi ve tereyağı kalıbı kurabiye/mutfak bağlamındadır; toz şeker kapalı paket olarak tasarım kararıyla temsil edilir, sargılı şekerden farklıdır. Fırın kapalı tek cihazdır, mutfak arka planı üretilmez. Halka kek kalıbı boş, mevcut düz fırın tepsisinden farklıdır. Çırpıcı çırpmak eyleminden çıkarılan el aletidir. İç lastik sönük tek halka olarak seçilir; bütün bisiklet, lastik pompası veya can simidi değildir. Küçük yama tek kauçuk parçadır; yara bandından farklıdır. Bu sahne aksesuarları tarif, tıbbi belge, tamir talimatı veya ölçülü teknik şema değildir. Mevcut R/K kartlar ve önceki yardımcı nesneler korunur. Tüm müfredat ve poz ayrıştırması bitmedi."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'sources':[v[0] for v in sources.values()],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
