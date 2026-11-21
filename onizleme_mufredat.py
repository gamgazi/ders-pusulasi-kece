#!/usr/bin/env python3
"""Müfredat resimlerini karşılaştırma sayfalarına dizer: sayfa başına 6 × 6 resim, altında kimlik ve Türkçe tarif.
Kullanım: python3 onizleme_mufredat.py <resim klasörü> <çıktı klasörü> [--parti "4-6 Kök"] [--tur nesne,sahne] [--ilk 36]
Gerekli: Pillow.  Yalnız dosyası olan resimler dizilir; sıra resimler.csv'deki sıradır."""
import sys, os, csv, textwrap
from PIL import Image, ImageDraw, ImageFont

arg = sys.argv[1:]
konum = [a for i, a in enumerate(arg) if not a.startswith('--') and (i == 0 or arg[i - 1] not in ('--parti', '--tur', '--ilk'))]
klasor, cikti = konum[0], konum[1]
parti = arg[arg.index('--parti') + 1] if '--parti' in arg else None
turler = arg[arg.index('--tur') + 1].split(',') if '--tur' in arg else None
ilk = int(arg[arg.index('--ilk') + 1]) if '--ilk' in arg else None
burada = os.path.dirname(os.path.abspath(__file__))
os.makedirs(cikti, exist_ok=True)
sat = [r for r in csv.DictReader(open(os.path.join(burada, 'resimler.csv'), encoding='utf-8'))
       if (not parti or r['parti'] == parti) and (not turler or r['tur'] in turler) and os.path.exists(os.path.join(klasor, r['dosya'] + '.png'))]
if ilk:
    sat = sat[:ilk]


def yazi(boy):
    for yol in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf', 'C:/Windows/Fonts/arialbd.ttf'):
        if os.path.exists(yol):
            return ImageFont.truetype(yol, boy)
    return ImageFont.load_default()


SUT, PX = 6, 300
PY = round(PX * 944 / 912)
KW, KH, ARA, UST = PX + 24, PY + 24 + 66, 10, 70
f, fk, fb = yazi(17), yazi(14), yazi(32)
ad = (parti or 'mufredat').lower().translate(str.maketrans('çğıöşü ', 'cgiosu-'))
for s in range(0, len(sat), SUT * SUT):
    dilim = sat[s:s + SUT * SUT]
    satir = (len(dilim) + SUT - 1) // SUT
    t = Image.new('RGBA', (ARA + SUT * (KW + ARA), UST + satir * (KH + ARA)), (143, 212, 97, 255))
    d = ImageDraw.Draw(t)
    d.text((ARA + 4, 16), f"{parti or 'Müfredat'} — sayfa {s // (SUT * SUT) + 1} ({s + 1}–{s + len(dilim)} / {len(sat)})", fill=(36, 48, 94), font=fb)
    for i, r in enumerate(dilim):
        x, y = ARA + (i % SUT) * (KW + ARA), UST + (i // SUT) * (KH + ARA)
        d.rounded_rectangle([x, y, x + KW - 1, y + KH - 1], radius=26, fill=(255, 255, 255, 255))
        im = Image.open(os.path.join(klasor, r['dosya'] + '.png')).convert('RGBA').resize((PX, PY), Image.LANCZOS)
        t.alpha_composite(im, (x + 12, y + 12))
        d.text((x + 14, y + PY + 16), r['kimlik'] + ' · ' + r['ilk_gectigi'], fill=(120, 130, 160), font=fk)
        for k, satir_yazi in enumerate(textwrap.wrap(r['resim'], 34)[:2]):
            d.text((x + 14, y + PY + 34 + k * 20), satir_yazi, fill=(36, 48, 94), font=f)
    yol = os.path.join(cikti, f'{ad}-{s // (SUT * SUT) + 1:02d}.png')
    t.convert('RGB').save(yol)
    print(yol, t.size, len(dilim), 'resim')
if not sat:
    print('dizilecek resim yok')
