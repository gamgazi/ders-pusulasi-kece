"""Append verified 7-9 Filiz object queue after record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE='pusula/ders-pusulasi/7-9-filiz.json'
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
    "ucak_yandan_001",
    "Tek uçak",
    "ulasim/ucak",
    2,
    "D5",
    "uçak",
    [
      "ucak"
    ]
  ],
  [
    "tren_lokomotif_001",
    "Tek tren lokomotifi",
    "ulasim/tren",
    5,
    "D5",
    "tren",
    [
      "tren",
      "lokomotif"
    ]
  ],
  [
    "hap_tek_001",
    "Tek kapsül hap",
    "saglik/hap",
    7,
    "D2",
    "hap",
    [
      "hap"
    ]
  ],
  [
    "igne_siringa_001",
    "Tek tıbbi şırınga",
    "saglik/siringa",
    7,
    "D7",
    "iğne",
    [
      "siringa",
      "igne"
    ]
  ],
  [
    "corba_kasesi_001",
    "Çorba dolu tek kâse",
    "yiyecek/corba",
    7,
    "D4",
    "çorba",
    [
      "corba"
    ]
  ],
  [
    "ihlamur_fincani_001",
    "Tek fincanda ıhlamur",
    "icecek/ihlamur",
    7,
    "D4",
    "ıhlamur",
    [
      "ihlamur_fincani",
      "ihlamur_cayi"
    ]
  ],
  [
    "kulube_tek_001",
    "Tek küçük kulübe",
    "mekan/kulube",
    8,
    "D5",
    "kulübe",
    [
      "kulube"
    ]
  ],
  [
    "cips_paketi_kapali_001",
    "Kapalı cips paketi",
    "yiyecek/cips",
    10,
    "D5",
    "cips",
    [
      "cips"
    ]
  ],
  [
    "camasir_sepeti_bos_001",
    "Boş çamaşır sepeti",
    "ev/camasir-sepeti",
    12,
    "D4",
    "çamaşır sepeti",
    [
      "camasir_sepeti"
    ]
  ],
  [
    "gorev_listesi_001",
    "Tek görev listesi",
    "ev/gorev-listesi",
    12,
    "D5",
    "görev listesi",
    [
      "gorev_listesi"
    ]
  ],
  [
    "bulasik_makinesi_kapali_001",
    "Kapalı bulaşık makinesi",
    "ev/bulasik-makinesi",
    12,
    "D5",
    "bulaşık makinesi",
    [
      "bulasik_makinesi"
    ]
  ],
  [
    "pirinc_paketi_kapali_001",
    "Kapalı pirinç paketi",
    "yiyecek/pirinc",
    13,
    "D4",
    "pirinç",
    [
      "pirinc"
    ]
  ],
  [
    "yag_sisesi_kapali_001",
    "Kapalı yemeklik yağ şişesi",
    "yiyecek/yag",
    13,
    "D5",
    "Yağımız bitti.",
    [
      "yag_sisesi",
      "yemeklik_yag"
    ]
  ],
  [
    "kitap_ayraci_001",
    "Tek kitap ayracı",
    "okul/kitap-ayraci",
    15,
    "D5",
    "kitap ayracı",
    [
      "kitap_ayraci"
    ]
  ],
  [
    "uzay_giysisi_bos_001",
    "Tek boş uzay giysisi",
    "uzay/uzay-giysisi",
    16,
    "D5",
    "uzay giysisi",
    [
      "uzay_giysisi"
    ]
  ],
  [
    "uzay_istasyonu_001",
    "Tek uzay istasyonu",
    "uzay/uzay-istasyonu",
    16,
    "D5",
    "uzay istasyonu",
    [
      "uzay_istasyonu"
    ]
  ],
  [
    "baglama_tek_001",
    "Tek bağlama",
    "muzik/baglama",
    17,
    "D2",
    "bağlama",
    [
      "baglama"
    ]
  ],
  [
    "kanun_tek_001",
    "Tek kanun",
    "muzik/kanun",
    17,
    "D2",
    "kanun",
    [
      "kanun"
    ]
  ],
  [
    "elektrogitar_tek_001",
    "Tek elektrogitar",
    "muzik/elektrogitar",
    17,
    "D3",
    "elektrogitar",
    [
      "elektrogitar"
    ]
  ],
  [
    "flut_tek_001",
    "Tek blok flüt",
    "muzik/flut",
    17,
    "D4",
    "flüt",
    [
      "flut"
    ]
  ],
  [
    "ney_tek_001",
    "Tek ney",
    "muzik/ney",
    17,
    "D4",
    "ney",
    [
      "ney"
    ]
  ],
  [
    "can_yelegi_001",
    "Tek can yeleği",
    "guvenlik/can-yelegi",
    18,
    "D4",
    "can yeleği",
    [
      "can_yelegi"
    ]
  ],
  [
    "emniyet_kemeri_001",
    "Tek bağlı emniyet kemeri",
    "guvenlik/emniyet-kemeri",
    18,
    "D4",
    "emniyet kemeri",
    [
      "emniyet_kemeri"
    ]
  ],
  [
    "kamyon_yandan_001",
    "Tek kamyon",
    "ulasim/kamyon",
    19,
    "D4",
    "kamyon",
    [
      "kamyon"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/filiz_7_9_kuyruk_kaniti.json'
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
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':"Kaynak sözcük/cümle birebir doğrulandı. Saksı yeni devrilmiş pozdur: mevcut kabul edilmiş saksı_bos_001 referans alınır; dik poz tekrar üretilmez. Mıknatıs, çivi ve musluk tek bağımsız nesnedir. Ödülün kupa biçimi ve zamanlayıcının mutfak tipi tasarım tercihidir, kaynakta bu alt biçim verilmez. Arı kovanında arı bulunmaz. Çöp torbası bağlı biçimiyle açık market poşetinden ayrılır. Kuş evi, dal yuvasından ayrı kapalı yapı nesnesidir. Oyun tahtası, afiş ve kartlardaki şekiller aynı kâğıdın çizimidir; çok nesneli kolaj üretilmez. Keçe kartlar korunur, ana hedef figürü yerine yardımcı kâğıt üretildiği açık tutulur. Tüm müfredat/poz ayrıştırması henüz tamamlanmadı."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blob_sha_verified':blob,'source':SOURCE,'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
