"""Append verified 7-9 Fidan object queue after record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE='pusula/ders-pusulasi/7-9-fidan.json'
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
    "hazine_sandigi_kapali_001",
    "Kapalı hazine sandığı",
    "masal/hazine-sandigi",
    3,
    "D2",
    "hazine",
    [
      "hazine",
      "sandik"
    ]
  ],
  [
    "kuyu_tek_001",
    "Tek kuyu",
    "masal/kuyu",
    3,
    "D5",
    "kuyu",
    [
      "kuyu"
    ]
  ],
  [
    "oklava_tek_001",
    "İnce oklava",
    "mutfak/oklava",
    6,
    "D3",
    "oklava",
    [
      "oklava"
    ]
  ],
  [
    "un_paketi_kapali_001",
    "Kapalı un paketi",
    "yiyecek/un",
    6,
    "D3",
    "un",
    [
      "un_paketi",
      "un_torbasi"
    ]
  ],
  [
    "harita_acik_001",
    "Açık gezi haritası",
    "esya/harita",
    8,
    "D3",
    "harita",
    [
      "harita"
    ]
  ],
  [
    "fare_bilgisayar_001",
    "Bilgisayar faresi",
    "teknoloji/fare",
    9,
    "D3",
    "fare",
    [
      "fare_bilgisayar",
      "bilgisayar_faresi"
    ]
  ],
  [
    "onluk_mutfak_001",
    "Mutfak önlüğü",
    "giysi/onluk",
    12,
    "D4",
    "önlük",
    [
      "onluk"
    ]
  ],
  [
    "traktor_yandan_001",
    "Traktör",
    "ulasim/traktor",
    12,
    "D5",
    "traktör",
    [
      "traktor"
    ]
  ],
  [
    "cadir_kazigi_tek_001",
    "Tek çadır kazığı",
    "kamp/cadir-kazigi",
    13,
    "D3",
    "çadır kazığı",
    [
      "cadir_kazigi"
    ]
  ],
  [
    "mangal_tek_001",
    "Tek mangal",
    "kamp/mangal",
    13,
    "D5",
    "mangal",
    [
      "mangal"
    ]
  ],
  [
    "manti_tek_001",
    "Tek mantı tanesi",
    "yiyecek/manti",
    15,
    "D1",
    "mantı",
    [
      "manti"
    ]
  ],
  [
    "dolma_tek_001",
    "Tek biber dolması",
    "yiyecek/dolma",
    15,
    "D2",
    "dolma",
    [
      "dolma"
    ]
  ],
  [
    "yufka_tek_001",
    "Tek yufka",
    "yiyecek/yufka",
    15,
    "D7",
    "yufka",
    [
      "yufka"
    ]
  ],
  [
    "baston_tek_001",
    "Tek baston",
    "esya/baston",
    16,
    "D3",
    "Bu dedemin bastonu.",
    [
      "baston"
    ]
  ],
  [
    "mama_kabi_bos_001",
    "Boş mama kabı",
    "esya/mama-kabi",
    16,
    "D3",
    "Kedinin mama kabı boş.",
    [
      "mama_kabi"
    ]
  ],
  [
    "kayip_esya_kutusu_bos_001",
    "Boş kayıp eşya kutusu",
    "okul/kayip-esya-kutusu",
    16,
    "D4",
    "kayıp eşya kutusu",
    [
      "kayip_esya"
    ]
  ],
  [
    "tasma_tek_001",
    "Tek köpek tasması",
    "esya/tasma",
    16,
    "D5",
    "köpeğin tasması",
    [
      "tasma"
    ]
  ],
  [
    "pil_tek_001",
    "Tek pil",
    "esya/pil",
    17,
    "D2",
    "pil",
    [
      "pil"
    ]
  ],
  [
    "cam_sise_bos_001",
    "Boş cam şişe",
    "esya/cam-sise",
    17,
    "D3",
    "cam şişe",
    [
      "cam_sise"
    ]
  ],
  [
    "bez_canta_bos_001",
    "Boş bez alışveriş çantası",
    "esya/bez-canta",
    17,
    "D4",
    "bez çanta",
    [
      "bez_canta"
    ]
  ],
  [
    "forma_tek_001",
    "Tek spor forması",
    "giysi/forma",
    18,
    "D7",
    "forma",
    [
      "forma"
    ]
  ],
  [
    "beslenme_cantasi_kapali_001",
    "Kapalı beslenme çantası",
    "okul/beslenme-cantasi",
    19,
    "D4",
    "beslenme çantası",
    [
      "beslenme_cantasi"
    ]
  ],
  [
    "mikrofon_tek_001",
    "Tek mikrofon",
    "teknoloji/mikrofon",
    20,
    "D6",
    "mikrofon",
    [
      "mikrofon"
    ]
  ],
  [
    "gazete_acik_001",
    "Açık gazete",
    "esya/gazete",
    1,
    "D4",
    "Babam gazete okurken kapı çaldı.",
    [
      "gazete"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/fidan_7_9_kuyruk_kaniti.json'
if all(s[0] in oldids for s in specs):
    print(json.dumps({'already_appended':True,'proof_preserved':proof.exists()}));raise SystemExit(0)
raw=(BASE/'work/source'/SOURCE).read_bytes()
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
expected=subprocess.check_output(['git','rev-parse','HEAD:'+SOURCE],cwd=REPO,text=True).strip()
assert blob==expected, 'Source Git blob mismatch'
source=json.loads(raw);cards=read(BASE/'work/source/kartlar.json')
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
for aid,title,cat,un,ln,term,aliases in specs:
    if aid in oldids:continue
    ui=next(i for i,u in enumerate(source['uniteler']) if u['no']==un);u=source['uniteler'][ui]
    di=next(i for i,d in enumerate(u['dersler']) if d['kod']==ln);d=u['dersler'][di]
    locs=[p for p,v in leaves(d) if v==term];assert locs,aid+' missing source evidence'
    historical=[x['record'] for x in h if any(matches(a,x.get('asset_name','')+' '+x['record']) for a in aliases)]
    existing=[x['id'] for x in q['items']+new if any(matches(a,x['id']) for a in aliases)]
    files=[x for x in canonical if any(matches(a,x) for a in aliases)]
    assert not historical and not existing and not files, (aid,historical,existing,files)
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':"Kaynak sözcük/cümle birebir doğrulandı; mevcut keçe kartları korunur. Hazine kapalı sandıkla temsil edilen bir yardımcı tasarım tercihidir, hazinenin kendisi veya dolu set olarak sayılmaz. Oklava ince sapsız çubuk biçimiyle merdaneden; bez çanta dikilmiş sap/torba biçimiyle mevcut plastik poşetten; beslenme çantası küçük kutu gövdesiyle sırt çantasından ayrılmalı. Un paketli, mantı/dolma/yufka tek parça yiyecek olarak; kuyu bağlı tek yapı olarak üretilecek. Fare bilgisayar aygıtıdır, hayvan değildir. Gazete/baston/mama kabı/tasma kaynak cümlede açıkça geçen nesnelerdir. R/K kartlar tekrar üretilmez. Her çıktı tek nesne PNG; tüm müfredat tamamlandı iddiası yok."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blob_sha_verified':blob,'source':SOURCE,'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
