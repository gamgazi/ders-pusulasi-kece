"""Append exact Fidan source evidence after canonical record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE='pusula/ders-pusulasi/4-6-fidan.json'
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
    "duduk_tek_001",
    "Düdük",
    "oyun/duduk",
    14,
    "D3",
    "düdük",
    [
      "duduk"
    ]
  ],
  [
    "zar_tek_001",
    "Zar",
    "oyun/zar",
    14,
    "D4",
    "zar",
    [
      "zar"
    ]
  ],
  [
    "roket_duran_001",
    "Ateşsiz duran roket",
    "uzay/roket",
    16,
    "D1",
    "roket",
    [
      "roket"
    ]
  ],
  [
    "kask_uzay_001",
    "Boş astronot kaskı",
    "uzay/kask",
    16,
    "D5",
    "kask",
    [
      "kask"
    ]
  ],
  [
    "teleskop_tek_001",
    "Teleskop",
    "uzay/teleskop",
    16,
    "D5",
    "teleskop",
    [
      "teleskop"
    ]
  ],
  [
    "uzay_gemisi_tek_001",
    "Uzay gemisi",
    "uzay/uzay-gemisi",
    16,
    "D7",
    "uzay gemisi",
    [
      "uzay_gemisi"
    ]
  ],
  [
    "davetiye_tek_001",
    "Katlı davetiye",
    "kutlama/davetiye",
    17,
    "D3",
    "davetiye",
    [
      "davetiye"
    ]
  ],
  [
    "pasta_butun_001",
    "Bütün pasta",
    "yiyecek/pasta",
    17,
    "D4",
    "pasta",
    [
      "pasta"
    ]
  ],
  [
    "seker_sargili_001",
    "Sargılı şeker",
    "yiyecek/seker",
    18,
    "D1",
    "şeker",
    [
      "seker"
    ]
  ],
  [
    "hediye_paket_001",
    "Hediye paketi",
    "kutlama/hediye",
    18,
    "D2",
    "hediye",
    [
      "hediye"
    ]
  ],
  [
    "kolonya_sisesi_001",
    "Kolonya şişesi",
    "bakim/kolonya",
    18,
    "D4",
    "kolonya",
    [
      "kolonya"
    ]
  ],
  [
    "lokum_tek_001",
    "Tek lokum",
    "yiyecek/lokum",
    18,
    "D4",
    "lokum",
    [
      "lokum"
    ]
  ],
  [
    "zil_kapi_001",
    "Kapı zili düğmesi",
    "ev/kapi-zili",
    13,
    "D3",
    "kapı zili",
    [
      "zil_kapi",
      "kapi_zili"
    ]
  ],
  [
    "tirnak_makasi_001",
    "Tırnak makası",
    "bakim/tirnak-makasi",
    11,
    "D3",
    "tırnak makası",
    [
      "tirnak_makasi"
    ]
  ],
  [
    "bilet_tek_001",
    "Bilet",
    "seyahat/bilet",
    5,
    "D6",
    "bilet",
    [
      "bilet"
    ]
  ],
  [
    "pasaport_kapali_001",
    "Kapalı pasaport",
    "seyahat/pasaport",
    5,
    "D6",
    "pasaport",
    [
      "pasaport"
    ]
  ],
  [
    "utu_tek_001",
    "Ütü",
    "ev/utu",
    7,
    "D3",
    "ütü yapmak",
    [
      "utu"
    ]
  ],
  [
    "camasir_makinesi_001",
    "Kapalı çamaşır makinesi",
    "ev/camasir-makinesi",
    7,
    "D3",
    "çamaşır yıkamak",
    [
      "camasir_makinesi"
    ]
  ],
  [
    "mandal_tek_001",
    "Tek mandal",
    "ev/mandal",
    7,
    "D3",
    "çamaşır asmak",
    [
      "mandal"
    ]
  ],
  [
    "cop_kovasi_kapali_001",
    "Kapalı çöp kovası",
    "ev/cop-kovasi",
    7,
    "D3",
    "çöpü çıkarmak",
    [
      "cop_kovasi"
    ]
  ],
  [
    "paten_tek_001",
    "Tek tekerlekli paten",
    "oyun/paten",
    8,
    "D5",
    "paten kaymak",
    [
      "paten"
    ]
  ],
  [
    "ip_atlama_001",
    "Atlama ipi",
    "oyun/atlama-ipi",
    8,
    "D7",
    "ip atlamak",
    [
      "ip_atlama",
      "atlama_ipi"
    ]
  ],
  [
    "merdiven_basamak_001",
    "Üç basamaklı merdiven",
    "ev/merdiven",
    19,
    "D4",
    "merdiven",
    [
      "merdiven"
    ]
  ],
  [
    "akvaryum_bos_001",
    "Boş akvaryum",
    "ev/akvaryum",
    20,
    "D4",
    "akvaryum",
    [
      "akvaryum"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/fidan_ikinci_kuyruk_kaniti.json'
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
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':aid in ['utu_tek_001','camasir_makinesi_001','mandal_tek_001','cop_kovasi_kapali_001','paten_tek_001','ip_atlama_001'],'semantic_review':'Eylem sözcüklerinden türetilen yardımcı nesneler ayrıca işaretlendi; kaynakta birebir nesne adı varmış gibi sayılmaz. Kapı zili kapıdan, tırnak makası mevcut makastan, çöp kovası mevcut su kovasından farklı. Merdiven güvenli üç basamaklı tek yapı; akvaryum boş, mevcut balık içerilmez. Roket ve uzay gemisi ayrı tasarımlar; mevcut gezegenler tekrar üretilmez.'})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blob_sha_verified':blob,'source':SOURCE,'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
