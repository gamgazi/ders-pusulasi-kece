"""Append verified 10-12 Agac, Cinar, Orman object queue after record/file reconciliation."""
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
    "oyun_kolu_001",
    "Tek oyun kumandası",
    "teknoloji/oyun-kolu",
    "10-12-agac",
    8,
    "D3",
    "oyun kolu",
    [
      "oyun_kolu",
      "oyun_kumandasi"
    ]
  ],
  [
    "robot_kol_001",
    "Tek tabanlı robot kol",
    "teknoloji/robot-kol",
    "10-12-cinar",
    11,
    "D3",
    "robot kol",
    [
      "robot_kol"
    ]
  ],
  [
    "kutuphane_karti_001",
    "Tek örnek kütüphane kartı",
    "kirtasiye/kutuphane-karti",
    "10-12-orman",
    8,
    "D2",
    "kütüphane kartı",
    [
      "kutuphane_karti"
    ]
  ],
  [
    "ansiklopedi_kapali_001",
    "Tek kapalı ansiklopedi",
    "kirtasiye/ansiklopedi",
    "10-12-orman",
    12,
    "D2",
    "ansiklopedi",
    [
      "ansiklopedi"
    ]
  ],
  [
    "goktasi_tek_001",
    "Tek düşmüş göktaşı",
    "uzay/goktasi",
    "10-12-orman",
    12,
    "D4",
    "göktaşı",
    [
      "goktasi"
    ]
  ],
  [
    "tekerlekli_sandalye_bos_001",
    "Tek boş tekerlekli sandalye",
    "ulasim/tekerlekli-sandalye",
    "10-12-orman",
    15,
    "D3",
    "tekerlekli sandalye",
    [
      "tekerlekli_sandalye"
    ]
  ],
  [
    "rampa_tek_001",
    "Tek kısa erişim rampası",
    "yapi/rampa",
    "10-12-orman",
    15,
    "D1",
    "rampa",
    [
      "rampa"
    ]
  ],
  [
    "asansor_kapali_001",
    "Tek kapalı asansör kapısı",
    "yapi/asansor",
    "10-12-orman",
    15,
    "D1",
    "asansör",
    [
      "asansor"
    ]
  ],
  [
    "takvim_masa_001",
    "Tek masa takvimi",
    "kirtasiye/takvim",
    "10-12-cinar",
    6,
    "D2",
    "takvim",
    [
      "takvim"
    ]
  ],
  [
    "oneri_kutusu_kapali_001",
    "Tek kapalı öneri kutusu",
    "okul/oneri-kutusu",
    "10-12-agac",
    1,
    "D4",
    "öneri kutusu",
    [
      "oneri_kutusu"
    ]
  ],
  [
    "kale_duvari_tek_001",
    "Tek kale duvarı parçası",
    "yapi/kale-duvari",
    "10-12-agac",
    7,
    "D3",
    "kale duvarı",
    [
      "kale_duvari"
    ]
  ],
  [
    "buzul_tek_001",
    "Tek karasal buzul dili",
    "doga/buzul",
    "10-12-agac",
    5,
    "D4",
    "buzul",
    [
      "buzul"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/agac_cinar_orman_10_12_kuyruk_kaniti.json'
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
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':"Kaynak sözcükler ve JSON konumları doğrulandı. Oyun kolu ekransız ayrı kumandadır; mevcut ekranlı el konsolundan farklıdır. Robot kol tabanlı mekanik tutucudur; insanımsı robot veya robot köpek değildir. Kütüphane kartı örnek ve boş kimlik alanlı; kredi kartı/izin belgesi değildir. Ansiklopedi bilgi kitabıdır; mevcut hikâye ve albümün tekrarı değildir. Göktaşı düşmüş koyu kabuklu tek kaya olarak temsil edilecek; genel taş ve alevli meteor birbirinden ayrılır, üretim öncesi birincil kaynakla biçimi doğrulanır. Tekerlekli sandalye boş, iki büyük arka ve iki küçük ön tekerlekli araç; bebek arabası veya sıradan sandalye değildir. Rampa tek eğimli platform, asansör kapalı çift sürgülü kapı ünitesi; bina/oda arka planı üretilmez. Takvim genel planlama nesnesidir; belirli tarihe göre gün doğruluğu gerekiyorsa ayrıca doğrulanır. Öneri kutusu fikir iletme işlevi ve etiketiyle bağış kutusundan farklıdır. Kale duvarı tek bağımsız sur parçası, mevcut bütün kalenin yeniden üretimi değildir. Buzul karada akan geniş buz dili olarak hazırlanır; eski eriyen buz küpü pozlarını veya yüzen buzdağını tekrar etmez. Çizimler sahne nesnesidir, teknik kurulum veya kullanım standardı şeması değildir. Mevcut R/K kartlar korunur; tüm müfredat ve poz ayrıştırması bitmedi."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'sources':[v[0] for v in sources.values()],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
