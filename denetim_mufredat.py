#!/usr/bin/env python3
"""Müfredat resimlerinin teslim denetimi (yalnız teknik ölçüler).
Kullanım: python3 denetim_mufredat.py [resim klasörü=mufredat-kece] [--parti "4-6 Kök"] [--tur nesne,sahne]
Gerekli: Pillow, numpy.

Her resim için:
  1. dosya var (adı resimler.csv'deki "dosya" sütunu + .png) · 912×944 · RGBA
  2. zemin saydam: dört köşe (24×24 px) boş; saydam alan tuvalin en az %25'i
  3. figür ortada ve tuvale sığıyor: alfa kutusunun her kenarı tuval kenarına ≥ 12 px; kutu merkezi tuval merkezine ≤ 60 px
  4. figür yeterince büyük: alfa kutusunun eni ya da boyu tuvalin ≥ %70'i
  5. malzeme var: ince doku (resim − bulanığı) ortalaması ≥ 3 (düz vektör çizimde ~0)
  6. kopya değil: iki ayrı kimliğin dosyası birebir aynı olamaz
Anlamı (tarifte ne yazıyorsa onu gösteriyor mu) bu betik ÖLÇEMEZ; onu gözle kontrol et.
"""
import sys, os, csv, hashlib, collections
import numpy as np
from PIL import Image, ImageFilter

burada = os.path.dirname(os.path.abspath(__file__))
arg = sys.argv[1:]
klasor = next((a for a in arg if not a.startswith('--')), os.path.join(burada, 'mufredat-kece'))
parti = arg[arg.index('--parti') + 1] if '--parti' in arg else None
turler = arg[arg.index('--tur') + 1].split(',') if '--tur' in arg else None
satirlar = [r for r in csv.DictReader(open(os.path.join(burada, 'resimler.csv'), encoding='utf-8'))
            if (not parti or r['parti'] == parti) and (not turler or r['tur'] in turler)]
W, H = 912, 944
ozet, gecen, yok, hatali = collections.Counter(), 0, [], []
izler = {}
for r in satirlar:
    yol = os.path.join(klasor, r['dosya'] + '.png')
    if not os.path.exists(yol):
        yok.append(r)
        continue
    im = Image.open(yol)
    hata = []
    if im.size != (W, H):
        hata.append(f'boy {im.size[0]}×{im.size[1]}')
    if im.mode != 'RGBA':
        hata.append(f'kip {im.mode}')
    a = np.asarray(im.convert('RGBA').resize((W, H)) if im.size != (W, H) else im.convert('RGBA'), dtype=np.float32)
    al = a[..., 3]
    kose = max(al[:24, :24].max(), al[:24, -24:].max(), al[-24:, :24].max(), al[-24:, -24:].max())
    bos = float((al < 8).mean())
    if kose > 8 or bos < .25:
        hata.append(f'zemin saydam değil (köşe alfa {int(kose)}, saydam alan %{bos * 100:.0f})')
    m = al > 128
    if not m.any():
        hata.append('boş resim')
    else:
        ys, xs = np.where(m)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        if min(x0, y0, W - 1 - x1, H - 1 - y1) < 12:
            hata.append(f'tuval kenarına dayanıyor (pay {int(min(x0, y0, W - 1 - x1, H - 1 - y1))} px)')
        if abs((x0 + x1) / 2 - W / 2) > 60 or abs((y0 + y1) / 2 - H / 2) > 60:
            hata.append(f'ortada değil ({int((x0 + x1) / 2 - W / 2)}, {int((y0 + y1) / 2 - H / 2)} px)')
        if max((x1 - x0) / W, (y1 - y0) / H) < .70:
            hata.append(f'küçük (kutu %{100 * (x1 - x0) / W:.0f} × %{100 * (y1 - y0) / H:.0f})')
        rgb = Image.fromarray(a.astype(np.uint8), 'RGBA').convert('RGB')
        doku = float(np.abs(np.asarray(rgb, dtype=np.float32) - np.asarray(rgb.filter(ImageFilter.GaussianBlur(3)), dtype=np.float32))[m].mean())
        if doku < 3:
            hata.append(f'malzeme yok: düz çizim gibi (ince doku {doku:.1f})')
    iz = hashlib.md5(open(yol, 'rb').read()).hexdigest()
    if iz in izler:
        hata.append('başka bir resmin kopyası: ' + izler[iz])
    izler.setdefault(iz, r['kimlik'])
    ozet[(r['parti'], r['tur'], not hata)] += 1
    if hata:
        hatali.append((r, hata))
    else:
        gecen += 1

for r, hata in hatali:
    print(f"✗ {r['dosya']:52s} {'; '.join(hata)}")
print(f"\n{len(satirlar)} satır · dosyası olan {len(satirlar) - len(yok)} · denetimden geçen {gecen} · hatalı {len(hatali)} · henüz üretilmemiş {len(yok)}")
partiler = collections.OrderedDict()
for r in satirlar:
    partiler.setdefault(r['parti'], collections.Counter())['toplam'] += 1
for (p, t, ok), n in ozet.items():
    partiler[p]['geçen' if ok else 'hatalı'] += n
for p, c in partiler.items():
    print(f"  {p:14s} toplam {c['toplam']:4d} · geçen {c['geçen']:4d} · hatalı {c['hatalı']:3d} · kalan {c['toplam'] - c['geçen'] - c['hatalı']:4d}")
sys.exit(0 if not hatali else 1)
