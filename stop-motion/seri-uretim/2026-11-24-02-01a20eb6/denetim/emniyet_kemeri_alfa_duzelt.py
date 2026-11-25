"""Inspected two seat-belt mounting-eye openings; alpha-only, no redraw or RGB edit."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
root=Path(__file__).resolve().parent.parent
src=root/'adaylar/emniyet_kemeri_001/r01/emniyet_kemeri_001_r01.png'
dst=root/'teknik-islem/emniyet_kemeri_001_alfa_bosluk.png'
if dst.exists():raise SystemExit('Refusing overwrite')
im=Image.open(src).convert('RGBA');a=np.array(im);before=a.copy()
roi=np.zeros(a.shape[:2],dtype=bool);roi[100:860,280:510]=True
white=(a[:,:,:3].min(axis=2)>160)&(a[:,:,3]>220)&roi
lab,n=ndimage.label(white)
holes=np.zeros(roi.shape,dtype=bool);regions=[]
for seedx,seedy in [(452,154),(342,808)]:
    label=int(lab[seedy,seedx])
    if label==0:raise SystemExit('Seed outside inspected white opening')
    region=lab==label
    area=int(region.sum())
    if not 1000<area<1300:raise SystemExit('Unexpected region; manual inspection required')
    inside=ndimage.binary_erosion(region,structure=np.ones((3,3)),iterations=3)
    if inside.sum()<30:raise SystemExit('Opening too small')
    holes|=inside;regions.append({'seed':[seedx,seedy],'white_region_pixels':area,'transparent_pixels':int(inside.sum()),'white_margin_pixels':3})
a[holes,3]=0
assert np.array_equal(a[:,:,:3],before[:,:,:3])
assert np.array_equal(a[~holes],before[~holes])
Image.fromarray(a,'RGBA').save(dst)
proof={'authorization':'Yerel teknik düzeltmeyi uygula','operation':'alpha-only removal of two visually inspected seat-belt mounting-eye white plugs; retain 3px paper margin','source':str(src.relative_to(root)),'target':str(dst.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'target_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'all_rgb_pixels_unchanged':True,'pixels_outside_holes_unchanged':True,'regions':regions,'changed_alpha_pixels':int(holes.sum()),'upscaled':False}
(root/'denetim/emniyet_kemeri_alfa_bosluk_kaniti.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(proof,ensure_ascii=False))
