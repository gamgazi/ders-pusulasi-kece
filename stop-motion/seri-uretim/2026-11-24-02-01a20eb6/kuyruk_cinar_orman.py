"""Append verified 7-9 Cinar and 4-6 Orman object queue after record/file reconciliation."""
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
    "deney_tupu_tek_001",
    "Tek deney tüpü",
    "bilim/deney-tupu",
    "7-9-cinar",
    5,
    "D3",
    "deney tüpü",
    [
      "deney_tupu"
    ]
  ],
  [
    "kamera_video_001",
    "Tek video kamera",
    "teknoloji/video-kamera",
    "7-9-cinar",
    8,
    "D2",
    "kamera",
    [
      "kamera"
    ]
  ],
  [
    "kale_tas_001",
    "Tek taş kale",
    "mekan/tas-kale",
    "7-9-cinar",
    9,
    "D1",
    "kale",
    [
      "kale_tas",
      "tas_kale"
    ]
  ],
  [
    "gaz_lambasi_001",
    "Tek gaz lambası",
    "ev/gaz-lambasi",
    "7-9-cinar",
    9,
    "D3",
    "gaz lambası",
    [
      "gaz_lambasi"
    ]
  ],
  [
    "at_arabasi_bos_001",
    "Boş at arabası gövdesi",
    "ulasim/at-arabasi",
    "7-9-cinar",
    9,
    "D3",
    "at arabası",
    [
      "at_arabasi"
    ]
  ],
  [
    "brosur_acik_001",
    "Tek açık broşür",
    "kagit/brosur",
    "7-9-cinar",
    12,
    "D3",
    "broşür",
    [
      "brosur"
    ]
  ],
  [
    "ses_kayit_cihazi_001",
    "Tek ses kayıt cihazı",
    "teknoloji/ses-kayit-cihazi",
    "7-9-cinar",
    14,
    "D3",
    "ses kaydı cihazı",
    [
      "ses_kayit",
      "ses_kaydi"
    ]
  ],
  [
    "not_defteri_001",
    "Tek not defteri",
    "kagit/not-defteri",
    "7-9-cinar",
    14,
    "D3",
    "not defteri",
    [
      "not_defteri"
    ]
  ],
  [
    "cay_bardagi_001",
    "Tek çay bardağı",
    "icecek/cay-bardagi",
    "7-9-cinar",
    15,
    "D3",
    "çay bardağı",
    [
      "cay_bardagi"
    ]
  ],
  [
    "kask_bisiklet_001",
    "Tek bisiklet kaskı",
    "guvenlik/bisiklet-kaski",
    "7-9-cinar",
    16,
    "D3",
    "kask",
    [
      "kask_bisiklet",
      "bisiklet_kaski"
    ]
  ],
  [
    "kumbara_tek_001",
    "Tek kumbara",
    "ev/kumbara",
    "7-9-cinar",
    18,
    "D1",
    "kumbara",
    [
      "kumbara"
    ]
  ],
  [
    "cuzdan_kapali_001",
    "Tek kapalı cüzdan",
    "aksesuar/cuzdan",
    "7-9-cinar",
    18,
    "D3",
    "cüzdan",
    [
      "cuzdan"
    ]
  ],
  [
    "bozuk_para_tek_001",
    "Tek bozuk para",
    "para/bozuk-para",
    "7-9-cinar",
    18,
    "D3",
    "bozuk para",
    [
      "bozuk_para",
      "madeni_para"
    ]
  ],
  [
    "nazar_boncugu_001",
    "Tek nazar boncuğu",
    "kultur/nazar-boncugu",
    "4-6-orman",
    8,
    "D2",
    "nazar boncuğu",
    [
      "nazar"
    ]
  ],
  [
    "kurabiye_tek_001",
    "Tek kurabiye",
    "yiyecek/kurabiye",
    "4-6-orman",
    9,
    "D2",
    "son kurabiye",
    [
      "kurabiye"
    ]
  ],
  [
    "tuy_tek_001",
    "Tek kuş tüyü",
    "doga/tuy",
    "4-6-orman",
    10,
    "D5",
    "tüy",
    [
      "tuy"
    ]
  ],
  [
    "findik_tek_001",
    "Tek fındık",
    "yiyecek/findik",
    "4-6-orman",
    18,
    "D3",
    "fındık",
    [
      "findik"
    ]
  ],
  [
    "pecete_katli_001",
    "Tek katlı peçete",
    "ev/pecete",
    "4-6-orman",
    19,
    "D4",
    "peçete",
    [
      "pecete"
    ]
  ],
  [
    "fermuar_kapali_001",
    "Tek kapalı fermuar",
    "giyim/fermuar",
    "4-6-orman",
    19,
    "D5",
    "fermuar",
    [
      "fermuar"
    ]
  ],
  [
    "saman_balyasi_001",
    "Tek saman balyası",
    "doga/saman-balyasi",
    "4-6-orman",
    11,
    "D3",
    "saman",
    [
      "saman_balyasi",
      "saman_demeti"
    ]
  ],
  [
    "robot_tek_001",
    "Tek oyuncak biçimli robot",
    "hayal/robot",
    "4-6-orman",
    7,
    "D1",
    "robot",
    [
      "robot_tek"
    ]
  ],
  [
    "ucan_araba_001",
    "Tek hayali uçan araba",
    "hayal/ucan-araba",
    "4-6-orman",
    7,
    "D2",
    "uçan araba",
    [
      "ucan_araba"
    ]
  ],
  [
    "uzay_evi_001",
    "Tek hayali uzay evi",
    "hayal/uzay-evi",
    "4-6-orman",
    7,
    "D2",
    "uzay evi",
    [
      "uzay_evi"
    ]
  ],
  [
    "robot_kopek_001",
    "Tek hayali robot köpek",
    "hayal/robot-kopek",
    "4-6-orman",
    7,
    "D3",
    "robot köpek",
    [
      "robot_kopek"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/cinar_orman_kuyruk_kaniti.json'
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
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':"Kaynak sözcük ve JSON konumu birebir doğrulandı. Tasarım seçimleri: kamera video kamera, kale taş kale (mevcut kumdan kaleden farklı); at arabası atsız tek gövde; kask bisiklet kaskı (mevcut uzay kaskından farklı); saman tek balya (mevcut saman evden farklı). Çay bardağı ince belli bardaktır; ıhlamur fincanının tekrarı değildir. Broşür ve not defteri mevcut masal kitabı, gazete ve görev listesinden farklı işlev/biçimdedir. Para hayali eğitim jetonu, gerçek banknot/kupür kopyası değildir. Gelecek nesneleri kaynakta hayal olarak geçer. Önceki R/K keçe kartları korunur. Tüm müfredat/poz ayrıştırması tamamlanmadı."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'sources':[v[0] for v in sources.values()],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
