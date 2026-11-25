from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
root=Path(__file__).resolve().parent.parent
src=root/'adaylar/kale_futbol_bos_001/r01/kale_futbol_bos_001_r01.png'
dst=root/'teknik-islem/kale_futbol_bos_001_alfa_bosluk.png'
assert not dst.exists()
a=np.array(Image.open(src).convert('RGBA'));before=a.copy()
white=(a[:,:,:3].min(2)>180)&(a[:,:,3]>220)
labels,n=ndimage.label(white)
regions=[]
for lid in range(1,n+1):
 r=labels==lid;size=int(r.sum())
 if size<80:continue
 y,x=np.where(r);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
 if box[0]>1180 and box[2]<1300 and box[1]>320 and box[3]<450:regions.append({'label':lid,'size':size,'bbox':box})
print(json.dumps(regions))
r=labels==45;assert int(r.sum())==543
y,x=np.where(r);assert [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]==[1232,363,1253,409]
inside=ndimage.binary_erosion(r,structure=np.ones((3,3)),iterations=3);assert 100<int(inside.sum())<350
a[inside,3]=0
assert np.array_equal(a[:,:,:3],before[:,:,:3])
assert np.array_equal(a[~inside],before[~inside])
Image.fromarray(a,'RGBA').save(dst)
proof={'authorization':'Yerel teknik düzeltmeyi uygula','operation':'alpha-only cleanup of one upper-right triangular net opening, preserve 3px white inner scissor margin','source':str(src.relative_to(root)),'target':str(dst.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'target_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'white_region_pixels':543,'changed_alpha_pixels':int(inside.sum()),'all_rgb_pixels_unchanged':True,'pixels_outside_holes_unchanged':True,'upscaled':False,'visual_review_required':True}
(root/'denetim/kale_futbol_alfa_bosluk_kaniti.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(proof,ensure_ascii=False))
