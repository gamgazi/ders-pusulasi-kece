"""Inspected left leg/runner opening; alpha-only, no RGB changes."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
root=Path(__file__).resolve().parent.parent
src=root/'adaylar/besik_bos_001/r01/besik_bos_001_r01.png'
dst=root/'teknik-islem/besik_bos_001_alfa_bosluk.png'
assert not dst.exists(), 'Refusing overwrite'
a=np.array(Image.open(src).convert('RGBA')); before=a.copy()
roi=np.zeros(a.shape[:2],bool);roi[680:840,420:750]=True
white=(a[:,:,:3].min(2)>120)&(a[:,:,3]>220)&roi
labels,n=ndimage.label(white); label=int(labels[710,475]); assert label>0
region=labels==label; assert int(region.sum())==5045
y,x=np.where(region); assert [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]==[430,698,629,827]
inside=ndimage.binary_erosion(region,structure=np.ones((3,3)),iterations=3)
assert 2000<int(inside.sum())<4500
a[inside,3]=0
assert np.array_equal(a[:,:,:3],before[:,:,:3])
assert np.array_equal(a[~inside],before[~inside])
Image.fromarray(a,'RGBA').save(dst)
proof={'authorization':'Yerel teknik düzeltmeyi uygula','operation':'alpha-only cleanup of one connected white plug spanning left leg gap and left runner wedge; retain 3px white paper inner margin','source':str(src.relative_to(root)),'target':str(dst.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'target_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'seed':[475,710],'white_region_pixels':5045,'changed_alpha_pixels':int(inside.sum()),'all_rgb_pixels_unchanged':True,'pixels_outside_holes_unchanged':True,'upscaled':False,'visual_review_required':True}
(root/'denetim/besik_bos_alfa_bosluk_kaniti.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(proof,ensure_ascii=False))
