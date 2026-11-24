"""Append exact Fidan source evidence after canonical record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE='pusula/ders-pusulasi/4-6-filiz.json'
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
    "bisiklet_tek_001",
    "Bisiklet",
    "oyun/bisiklet",
    3,
    "D2",
    "bisiklet",
    [
      "bisiklet"
    ]
  ],
  [
    "yapboz_parcasi_tek_001",
    "Tek yapboz parçası",
    "oyun/yapboz-parcasi",
    3,
    "D4",
    "yapboz",
    [
      "yapboz"
    ]
  ],
  [
    "oyun_hamuru_kapali_001",
    "Kapalı oyun hamuru kabı",
    "oyun/oyun-hamuru",
    3,
    "D5",
    "oyun hamuru",
    [
      "oyun_hamuru"
    ]
  ],
  [
    "mayo_tek_001",
    "Tek parça mayo",
    "giysi/mayo",
    9,
    "D3",
    "mayo",
    [
      "mayo"
    ]
  ],
  [
    "hirka_kapali_001",
    "Düğmeli hırka",
    "giysi/hirka",
    9,
    "D3",
    "hırka",
    [
      "hirka"
    ]
  ],
  [
    "ceket_tek_001",
    "Yakalı ceket",
    "giysi/ceket",
    9,
    "D3",
    "ceket",
    [
      "ceket"
    ]
  ],
  [
    "yagmurluk_kapali_001",
    "Kapüşonlu uzun yağmurluk",
    "giysi/yagmurluk",
    9,
    "D5",
    "yağmurluk",
    [
      "yagmurluk"
    ]
  ],
  [
    "kredi_karti_tek_001",
    "Temsili kredi kartı",
    "esya/kredi-karti",
    12,
    "D3",
    "kredi kartı",
    [
      "kredi_karti",
      "banka_karti"
    ]
  ],
  [
    "pijama_tulum_001",
    "Tek parça pijama tulumu",
    "giysi/pijama",
    13,
    "D4",
    "pijama",
    [
      "pijama"
    ]
  ],
  [
    "kumdan_kale_001",
    "Kumdan kale",
    "doga/kumdan-kale",
    15,
    "D5",
    "kumdan kale",
    [
      "kumdan_kale",
      "kum_kalesi"
    ]
  ],
  [
    "kum_havuzu_001",
    "Kum havuzu",
    "park/kum-havuzu",
    16,
    "D1",
    "kum havuzu",
    [
      "kum_havuzu"
    ]
  ],
  [
    "cesme_park_001",
    "Park çeşmesi",
    "park/cesme",
    16,
    "D4",
    "çeşme",
    [
      "cesme"
    ]
  ],
  [
    "olta_tek_001",
    "Tek olta",
    "kamp/olta",
    17,
    "D7",
    "olta",
    [
      "olta"
    ]
  ],
  [
    "piyano_tek_001",
    "Duvar piyanosu",
    "muzik/piyano",
    19,
    "D1",
    "piyano",
    [
      "piyano"
    ]
  ],
  [
    "zil_muzik_001",
    "Saplı el zili",
    "muzik/zil",
    19,
    "D1",
    "zil",
    [
      "zil_muzik",
      "el_zili",
      "zil_el"
    ]
  ],
  [
    "tuval_bos_001",
    "Boş resim tuvali",
    "sanat/tuval",
    19,
    "D3",
    "tuval",
    [
      "tuval"
    ]
  ],
  [
    "dans_ayakkabisi_tek_001",
    "Tek dans ayakkabısı",
    "giysi/dans-ayakkabisi",
    19,
    "D3",
    "dans ayakkabısı",
    [
      "dans_ayakkabisi",
      "bale_ayakkabisi"
    ]
  ],
  [
    "darbuka_tek_001",
    "Darbuka",
    "muzik/darbuka",
    19,
    "D4",
    "darbuka",
    [
      "darbuka"
    ]
  ],
  [
    "tef_tek_001",
    "Tef",
    "muzik/tef",
    19,
    "D4",
    "tef",
    [
      "tef"
    ]
  ],
  [
    "trompet_tek_001",
    "Trompet",
    "muzik/trompet",
    19,
    "D4",
    "trompet",
    [
      "trompet"
    ]
  ],
  [
    "maraka_tek_001",
    "Tek maraka",
    "muzik/maraka",
    19,
    "D7",
    "maraka",
    [
      "maraka",
      "marakas"
    ]
  ],
  [
    "kemence_tek_001",
    "Kemençe",
    "muzik/kemence",
    19,
    "D7",
    "kemençe",
    [
      "kemence"
    ]
  ],
  [
    "saksafon_tek_001",
    "Saksafon",
    "muzik/saksafon",
    19,
    "D7",
    "saksafon",
    [
      "saksafon"
    ]
  ],
  [
    "keman_tek_001",
    "Keman",
    "muzik/keman",
    19,
    "D7",
    "keman",
    [
      "keman"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/filiz_ikinci_kuyruk_kaniti.json'
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
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':"Kaynak nesne sözcüğü birebir doğrulandı; mevcut keçe kartları korunur. Yapboz tek parça ile, oyun hamuru kapalı kabıyla, pijama tek parça tulumla temsil edilir; tam set üretildiği iddia edilmez. Hırka/ceket/yağmurluk mevcut monttan yaka, ön kapanış, uzunluk ve yapıyla ayrılmalı. Müzik zili mevcut kapı zilinden farklıdır. Kredi kartı yalnız temsili nesne; gerçek kurum/kişi/kart bilgisi içermez. Çeşme tek mimari nesne; su ayrı hareket varlığıdır. Piyano bilgisayar klavyesinden farklıdır. Kemençe/keman yapıları ayrı denetlenecek; yay eklenmez. Her üretim tek nesne ve tek PNG."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blob_sha_verified':blob,'source':SOURCE,'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
