"""Inspected five fire truck ladder underside openings; alpha-only, no redraw or RGB edit."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
root=Path(__file__).resolve().parent.parent
src=root/'adaylar/itfaiye_araci_yandan_001/r05/itfaiye_araci_yandan_001_r05.png'
dst=root/'teknik-islem/itfaiye_araci_yandan_001_alfa_bosluk.png'
if dst.exists():raise SystemExit('Refusing overwrite')
im=Image.open(src).convert('RGBA');a=np.array(im);before=a.copy()
roi=np.zeros(a.shape[:2],dtype=bool);
for x0,y0,x1,y1 in [(624,344,650,373),(717,344,856,374),(868,344,1006,375),(1016,344,1173,375),(1243,344,1299,373)]:roi[y0:y1,x0:x1]=True
white=(a[:,:,:3].min(axis=2)>70)&(np.ptp(a[:,:,:3].astype(int),axis=2)<90)&roi
lab,n=ndimage.label(white)
holes=np.zeros(roi.shape,dtype=bool);regions=[]
for seedx,seedy in [(636,358),(780,358),(932,359),(1090,359),(1271,359)]:
    label=int(lab[seedy,seedx])
    if label==0:raise SystemExit('Seed outside inspected white opening')
    region=lab==label
    area=int(region.sum())
    if not 80<area<5000:raise SystemExit('Unexpected region; manual inspection required')
    inside=ndimage.binary_erosion(region,structure=np.ones((3,3)),iterations=3)
    if inside.sum()<15:raise SystemExit('Opening too small')
    holes|=inside;regions.append({'seed':[seedx,seedy],'white_region_pixels':area,'transparent_pixels':int(inside.sum()),'white_margin_pixels':3})
a[holes,3]=0
assert np.array_equal(a[:,:,:3],before[:,:,:3])
assert np.array_equal(a[~holes],before[~holes])
Image.fromarray(a,'RGBA').save(dst)
proof={'authorization':'Yerel teknik düzeltmeyi uygula','operation':'alpha-only removal of five visually inspected gray alpha residues beneath fire truck ladder; retain 3px paper margin','source':str(src.relative_to(root)),'target':str(dst.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'target_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'all_rgb_pixels_unchanged':True,'pixels_outside_holes_unchanged':True,'regions':regions,'changed_alpha_pixels':int(holes.sum()),'upscaled':False}
(root/'denetim/itfaiye_araci_yandan_alfa_bosluk_kaniti.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(proof,ensure_ascii=False))
